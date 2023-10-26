# Сервис сокращения ссылок

## Запуск проекта (для разработки)
Все упаковано в докер-контейнеры, и только порт Django-сервера виден наружу.
Если возникают ошибки, [обновите Docker](https://docs.docker.com/engine/install/).

```
$ git clone https://github.com/kuzmich/url-shortener-hemli.git
$ cd url-shortener-hemli

$ docker compose build web
$ docker compose up

# при первом запуске дождитесь инициализации базы данных
$ docker compose exec web pipenv run ./manage.py migrate
```

Откройте в браузере страницу по адресу http://127.0.0.1:8000/

## Настройки
В файле hemli/shrtnr/__init__.py есть несколько настроек:

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
