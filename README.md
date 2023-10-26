# Сервис сокращения ссылок
Архитектура проекта стандартная: генерация страницы на бэкенде (Python, Django),
хранение данных в MySQL, кэш на Redis. Проект оформлен как Python-пакет, что дает
возможность избежать проблем с путями (`pip install -e .`) и легко разворачивать
wheel-пакеты (`pip install build; build`).

В проекте используется стандартный функционал Django: сессии, кэш, шаблоны. На фронтэнде
используется Bootstrap 5 и пакет `django-bootstrap5`.

## Запуск проекта (для разработки)
Все упаковано в докер-контейнеры, и только порт Django-сервера виден наружу.
Если возникают ошибки при сборке, [обновите Docker](https://docs.docker.com/engine/install/). 

### Первый раз
```
$ git clone https://github.com/kuzmich/url-shortener-hemli.git
$ cd url-shortener-hemli

$ docker compose build web

# Дождитесь инициализации базы данных (может занять около минуты)
# Затем остановите контейнер (`Ctrl-C`)
$ docker compose up mysql

$ docker compose up

$ docker compose exec web pipenv run ./manage.py migrate
```

### Последующие разы
```
$ docker compose up
```

Откройте в браузере страницу по адресу http://127.0.0.1:8000/

## Запуск тестов
```
$ docker compose exec web pipenv run pytest -v tests/
```

## Настройки
В файле `hemli/shrtnr/__init__.py` есть несколько настроек:

- `SESSION_COOKIE_AGE`: сколько времени пользователь видит свои ссылки
- `LINKS_PER_PAGE`: количество ссылок на странице
- `SHORT_PATH_LEN`: длина ссылки (будет расти автоматически по мере заполнения базы)
- `CACHES['default']['TIMEOUT']`: на сколько кешируется ссылка

## Очистка
Т.к. сокращения привязаны к сессиям пользователей, то если удалить протухшую сессию,
сокращенные ссылки удалятся вместе с сессией.

**Удаление "протухших" сессий**
```
$ ./manage.py clearsessions
```
