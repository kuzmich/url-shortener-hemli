import logging
import secrets
import string

from django.contrib.sessions.models import Session
from django.core.cache import cache
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ShortenerForm
from .models import ShortLink


logger = logging.getLogger(__name__)


def main(request):
    if not request.session.session_key:
        request.session.create()
        
    session = Session.objects.get(session_key=request.session.session_key)
    
    if request.method == 'POST':
        form = ShortenerForm(request.POST)

        if form.is_valid():
            url = form.cleaned_data['url']
            path = form.cleaned_data['path']
            
            link = ShortLink(
                url=url,
                path=path if path else generate_path(),
            )
            link.save()
            link.sessions.add(session)

            cache.set(f's-{path}', url)
            
            return redirect('main')
        else:
            logger.warning('Invalid form input: %s', form.errors.as_json())
    else:
        form = ShortenerForm()

    my_links = session.short_links.all()
    
    return render(
        request,
        'main.html',
        {'form': form, 'my_links': my_links}
    )


def redirect_to_full(request, short_path):
    if url := cache.get(f's-{short_path}'):
        return redirect(url)
    else:
        link = get_object_or_404(ShortLink, path=short_path)
        ShortLink.objects.filter(id=link.id).update(num_views=F('num_views') + 1)
        return redirect(link.url)


def generate_path(path_len=3):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(path_len))
