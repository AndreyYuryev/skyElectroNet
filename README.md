## Сеть Продаж Электроники
Этот проект представляет собой веб-приложение на базе Django для управления сетью продаж электроники. Приложение включает в себя API-интерфейс, админ-панель и иерархическую структуру узлов сети.

Технические Требования
Python 3.8+
Django 3+
Django REST Framework (DRF) 3.10+
PostgreSQL 10+

### Установка

Клонирование Репозитория
> git clone https://github.com/AndreyYuryev/skyElectroNet.git

>cd skyElectroNet

Создание и Активация Виртуального Окружения
>python -m venv venv

>source venv/bin/activate #В Windows используйте `venv\Scripts\activate`

Установка Зависимостей
>pip install -r requirements.txt

Применение Миграций
>python manage.py migrate

Запуск Сервера Разработки
>python manage.py runserver

## Использование
### Админ-Панель
Доступ к админ-панели Django можно получить по адресу http://127.0.0.1:8000/admin/, войдите, используя учетные данные суперпользователя. 

Отсюда вы можете управлять продуктами, пользователями, компаниями(поставщиками и получателями), элементами сети поставки, поставками, задолженностью и платежами.
Списание задолженности выполняется действием "Списать задолженность перед поставщиком/Оплатить". После этого долг обнуляется и появляется запись о списании задолженности.
Компанию (поставщика/покупателя), продукт и элементы сети нельзя удалить - только деактивировать. При деактивации продукта, компании или элемента поставки деактивируется вся нижестоящая цепочка поставщиков.
Первый элемент в цепи поставщиков всегда завод-производитель продукта. Завод не может выступать в роли получателя продукта. Цепочка поставщиков может быть сколь угодно большая при условии что в каждом элементе может быть только один поставщик, а первый элемент всегда завод-производитель.
Уровень в иерархии - поставка с завода всегда 1 и далее +1 к каждому элементу.

API Эндпоинты
API позволяет выполнять CRUD операции над компаниями, сетью поставщиков, задолженностью и продуктами. Доступ к API имеют только активные пользователи.

- Продукт: http://127.0.0.1:8000/api/v1/product/ при создании http://127.0.0.1:8000/api/v1/product/create/
- Компания: http://127.0.0.1:8000/api/v1/company/ при создании http://127.0.0.1:8000/api/v1/company/create/
Фильтрация по стране: http://127.0.0.1:8000/api/v1/company/?country=Россия
- Задолженность: http://127.0.0.1:8000/api/v1/debt/ - только на просмотр
- Поставка: http://127.0.0.1:8000/api/v1/delivery/ - только создание и посмотр
- Поставщики: http://127.0.0.1:8000/api/v1/deliverynet/ при создании http://127.0.0.1:8000/api/v1/deliverynet/create/
- Пользователи: http://127.0.0.1:8000/api/v1/users/

Создание админа и двух пользователей:
> python manage.py create_su
> 
> python manage.py create_user

Заполнение тестовыми данными:
> python manage.py create_data


