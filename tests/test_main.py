from django.test import Client
import pytest

from hemli.shrtnr.models import ShortLink


@pytest.mark.django_db
def test_can_shorten_url(client: Client):
    # Пусть на сайт зашел новый пользователь
    
    # Когда он ввел длинный URL и нажал кнопку Сократить
    long_url = 'https://docs.google.com/document/d/1La9LOrj8qdpt4CVJOYAhuIrK0L0SOVIxfYp4CC5yU3A/edit'
    resp = client.post('/', {'url': long_url}, follow=True)
    assert resp.status_code == 200  # 302
    
    # То видит сокращенный URL
    short_links = resp.context['my_links']
    assert short_links.count() == 1
    
    short_link = short_links[0]
    assert short_link.url == long_url
    assert len(short_link.path) == 3


@pytest.mark.django_db
def test_can_use_custom_path(client: Client):
    # Пусть пользователь хочет сократить URL, но использовать свое сокращение
    
    # Когда он вводит это сокращение в форму
    long_url = 'https://docs.google.com/document/d/1La9LOrj8qdpt4CVJOYAhuIrK0L0SOVIxfYp4CC5yU3A/edit'
    custom_path = 'mME'
    
    resp = client.post('/', {'url': long_url, 'path': custom_path})
    assert resp.status_code == 302
    
    # Сервис создает короткий URL с этим сокращением
    assert ShortLink.objects.filter(url=long_url, path=custom_path).exists()


@pytest.mark.django_db
def test_cant_use_already_used_custom_path(client: Client):
    # Пусть пользователь хочет использовать свое сокращение,
    # но оно уже использовано кем-то другим
    ShortLink.objects.create(url='https://some.long/url', path='OMG')
    
    # Когда он вводит это сокращение в форму
    long_url = 'https://docs.google.com/document/d/1La9LOrj8qdpt4CVJOYAhuIrK0L0SOVIxfYp4CC5yU3A/edit'
    custom_path = 'OMG'
    
    resp = client.post('/', {'url': long_url, 'path': custom_path})
    assert resp.status_code == 200
    
    # То видит сообщение об ошибке
    assert "Такое сокращение уже занято" in resp.content.decode()


@pytest.mark.django_db
def test_can_shorten_already_shortened_url(client: Client):
    # Пусть пользователь хочет сократить URL,
    # Но кто-то уже сокращал такой URl
    long_url = 'https://docs.google.com/document/d/1La9LOrj8qdpt4CVJOYAhuIrK0L0SOVIxfYp4CC5yU3A/edit'
    ShortLink.objects.create(url=long_url, path='OMG')
    
    # Когда он вводит этот URL в форму
    resp = client.post('/', {'url': long_url})
    assert resp.status_code == 302
    
    # Сервис создает еще одно сокращение для такого URL
    assert ShortLink.objects.filter(url=long_url).count() == 2


@pytest.mark.django_db
def test_can_follow_short_url(client: Client):
    # Пусть в базе есть сокращенный URL
    long_url = 'https://docs.google.com/document/d/1La9LOrj8qdpt4CVJOYAhuIrK0L0SOVIxfYp4CC5yU3A/edit'
    short_path = 'aSd'
    ShortLink.objects.create(url=long_url, path=short_path)

    # Когда пользователь переходит по нему
    resp = client.get(f'/{short_path}')

    # Сервис делает редирект на оригинальный URL
    assert resp.status_code == 302
    assert resp.headers['location'] == long_url


@pytest.mark.django_db
def test_following_url_incr_views(client: Client):
    # Пусть в базе есть сокращенный URL
    long_url = 'https://docs.google.com/document/d/1La9LOrj8qdpt4CVJOYAhuIrK0L0SOVIxfYp4CC5yU3A/edit'
    short_path = 'aSd'
    short_link = ShortLink.objects.create(url=long_url, path=short_path)
    assert short_link.num_views == 0

    # Когда пользователь переходит по нему
    resp = client.get(f'/{short_path}')

    # Сервис увеличивает количество просмотров данного URL-а
    assert resp.status_code == 302
    short_link.refresh_from_db()
    assert short_link.num_views == 1


@pytest.mark.django_db
def test_cant_shorten_empty_url(client: Client):
    # Пусть злобный хацкер хочет хакнуть наш сервис
    # Когда он отправляет пустую строку вместо URL
    resp = client.post('/', {'url': ''})
    
    # Сервис сообщает об ошибке
    assert resp.status_code == 200
    assert 'Обязательное поле' in resp.content.decode()


@pytest.mark.django_db
def test_cant_shorten_non_url_str(client: Client):
    # Пусть злобный хацкер хочет хакнуть наш сервис
    # Когда он отправляет какую-нибудь строку вместо URL
    resp = client.post('/', {'url': 'блаблабла'})

    # Сервис сообщает об ошибке
    assert resp.status_code == 200
    assert 'Введите корректный URL' in resp.content.decode()


@pytest.mark.django_db
def test_cant_use_too_long_path(client: Client):
    # Пусть злобный хацкер хочет хакнуть наш сервис
    # Когда он отправляет слишком длинное сокращение
    resp = client.post('/', {'url': 'http://long.url/there', 'path': 'a' * 50})

    # Сервис сообщает об ошибке
    assert resp.status_code == 200
    assert 'Сокращение должно быть не длиннее 10 символов' in resp.content.decode()


@pytest.mark.django_db
def test_making_short_url_caches_it(client: Client):
    # Пусть пользователь создал короткий URL
    resp = client.post('/', {'url': 'http://long.url/here'})
    assert resp.status_code == 302

    short_link = ShortLink.objects.get()
    path = short_link.path
    short_link.delete()
    
    # Когда он переходит по этой ссылке
    # Сервер не обращается к базе, так как закешировал ссылку при создании
    resp = client.get(f'/{path}')
    assert resp.status_code == 302
    assert resp.headers['location'] == 'http://long.url/here'
