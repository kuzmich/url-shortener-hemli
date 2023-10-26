# Сервис сокращения ссылок

## Очистка
Т.к. сокращения привязаны к сессиям пользователей, то если удалить протухшую сессию,
сокращенные ссылки удалятся вместе с сессией.

**Удаление "протухших" сессий**
```
$ ./manage.py clearsessions
```
