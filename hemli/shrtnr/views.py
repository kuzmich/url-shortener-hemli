import secrets
import string

from django.db.models import F
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ShortenerForm
from .models import ShortLink


def main(request):
    if not request.session.session_key:
        request.session.create()
        
    session = Session.objects.get(session_key=request.session.session_key)
    
    if request.method == 'POST':
        form = ShortenerForm(request.POST)

        if form.is_valid():
            path = form.cleaned_data['path']
            link = ShortLink(
                url=form.cleaned_data['url'],
                path=path if path else generate_path(),
            )
            link.save()
            link.sessions.add(session)
            
            return redirect('main')
    else:
        form = ShortenerForm()

    my_links = session.short_links.all()
    
    return render(
        request,
        'main.html',
        {'form': form, 'my_links': my_links}
    )


def redirect_to_full(request, short_path):
    link = get_object_or_404(ShortLink, path=short_path)
    ShortLink.objects.filter(id=link.id).update(num_views=F('num_views') + 1)
    return redirect(link.url)


def generate_path(path_len=3):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(path_len))
