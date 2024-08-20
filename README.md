# Django/DRF/Djoser backend. API for make courses, lessons, groups etc.

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)

# Auth Endpoints

## /api/v1/auth/users/ ['POST']
Создание нового пользователя.

**Поля**: *username, password, first_name, last_name, email*

## /api/v1/auth/token/login/ ['POST']
Аутентификация и авторизация пользователя. Выдача токена.

**Headers**: *Authorization: Token ***your-token****

# Main Endpoints

## 1. api/v1/courses/ ['GET']
Список всех курсов с данными о них: ***названия уроков в курсе, процент покупок, 
процент заполнения групп, кол-во студентов, кол-во уроков***

## 2. /api/v1/courses/{course_id}/ ['GET']
Данные об определенном курсе.

## 3. /api/v1/courses/buy/ ['GET'] 
### Permisssions: IsAuthenticated
Список курсов, доступных к покупке (которые не находятся у пользователя в подписке).

## 4. /api/v1/courses/{course_id}/pay/ ['POST']
### Permisssions: IsAuthenticated
Оплата курса, т.е. добавление его в подписку пользователя.

### => /api/v1/courses/{course_id}/lessons/ ['GET']
#### Permissions: IsStudentOrIsAdmin
Список всех уроков курса со всеми данными: ***название, url***. Как и должно быть, открывается
пользователю после приобретения курса.


## 5. /api/v1/courses/{course_id}/groups/ ['GET']
### Permissions: IsAdminUser
Список групп определенного курса с информацией про студентов в них.


# P.S.
При создании курса создается 10 групп, принадлежащих этому курсу. При покупке
пользователем курса, находится группа с минимальным количеством студентов,
и пользователь автоматически заносится в эту группу. Таким образом реализовано
равномерное распределение пользователей по группам.

