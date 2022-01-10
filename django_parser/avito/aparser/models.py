from django.db import models


class Product(models.Model):
    title = models.TextField(
        verbose_name='Заголовок',
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
    )
    address = models.TextField(
        verbose_name='Адрес',
    )
    url = models.URLField(
        verbose_name='Ссылка на объявление',
        unique=True,
    )
    published_date = models.DateTimeField(
        verbose_name='Дата публикации',
    )

    class Meta:
        verbose_name = 'Купить'
        verbose_name_plural = 'Купить'


class Rent(models.Model):
    title = models.TextField(
        verbose_name='Заголовок',
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
    )
    srok = models.TextField(
        verbose_name='Срок'
    )
    address = models.TextField(
        verbose_name='Адрес',
    )
    url = models.URLField(
        verbose_name='Ссылка на объявление',
        unique=True,
    )
    published_date = models.DateTimeField(
        verbose_name='Дата публикации',
    )

    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренда'


class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='Внешний ID пользователя',
        unique=True,
    )
    name = models.TextField(
        verbose_name='Имя пользователя',
        null=True
    )

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Message(models.Model):
    profile = models.ForeignKey(
        to='aparser.Profile',
        verbose_name='Профиль',
        on_delete=models.PROTECT,
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    created_at = models.DateTimeField(
        verbose_name='Время получения',
        auto_now_add=True,
    )

    def __str__(self):
        return f'Сообщение {self.pk} от {self.profile}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
