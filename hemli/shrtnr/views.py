import logging
import secrets

from django.conf import settings
from django.contrib.sessions.models import Session
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ShortenerForm
from .models import ShortLink


logger = logging.getLogger(__name__)


def main(request):
    session_key = request.session.session_key
    if not session_key or not Session.objects.filter(session_key=session_key).exists():
        request.session.create()
        session_key = request.session.session_key
        
    session = Session.objects.get(session_key=session_key)
    
    if request.method == 'POST':
        form = ShortenerForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data['url']
            path = form.cleaned_data['path']

            link = create_short_link(url, path, session)
            
            cache.set(f's-{link.path}', url)
            return redirect('main')
        else:
            logger.warning('Invalid form input: %s', form.errors.as_json())
    else:
        form = ShortenerForm()

    my_links = session.short_links.order_by('-created_at')
    paginator = Paginator(my_links, settings.LINKS_PER_PAGE)
    page_obj = paginator.get_page(request.GET.get('page'))
    
    return render(
        request,
        'main.html',
        {'form': form, 'my_links': page_obj, 'page_obj': page_obj}
    )


def create_short_link(url, path, session):
    if path:
        link = ShortLink(url=url, path=path, session=session)
        link.save()
        return link
    
    num_generations = 0
    short_path_len = cache.get('short_path_len', settings.SHORT_PATH_LEN)

    while True:
        if num_generations >= 2:
            short_path_len += 1
            num_generations = 0

            if short_path_len > 10:
                raise Exception("Can't generate short path")
            
        path = generate_path(short_path_len)
        num_generations += 1
        
        logger.debug(
            "Generated path '%s' (round %d, path len: %d)",
            path, num_generations, short_path_len
        )
            
        try:
            with transaction.atomic():
                link = ShortLink(url=url, path=path, session=session)
                link.save()
            break
        except IntegrityError as e:
            logger.debug('%r', e)

    cache.set('short_path_len', short_path_len, None)

    return link


def generate_path(path_len=None):
    if path_len is None:
        path_len = settings.SHORT_PATH_LEN
    abc = settings.SHORT_PATH_ABC
    return ''.join(secrets.choice(abc) for _ in range(path_len))


def redirect_to_full(request, short_path):
    if url := cache.get(f's-{short_path}'):
        ShortLink.objects.filter(path=short_path).update(num_views=F('num_views') + 1)
        return redirect(url)
    else:
        link = get_object_or_404(ShortLink, path=short_path)
        ShortLink.objects.filter(id=link.id).update(num_views=F('num_views') + 1)
        return redirect(link.url)
