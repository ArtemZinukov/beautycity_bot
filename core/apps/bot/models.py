from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    tg_id = models.IntegerField(unique=True, verbose_name='Телеграмм id клиента')
    username = models.CharField(max_length=50, verbose_name='Имя клиента')
    phone_number = PhoneNumberField(max_length=12, verbose_name='Номер телефона')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Service(models.Model):
    title = models.CharField(max_length=100, verbose_name='Название процедуры')
    price = models.DecimalField(max_digits=6, decimal_places=0, verbose_name='Цена')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Процедура"
        verbose_name_plural = "Процедуры"


class Master(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя мастера')
    services = models.ManyToManyField(Service, verbose_name='Услуга')
    salons = models.ManyToManyField("Salon", verbose_name='Салон')

    def __str__(self):
        return self.name

    def get_services(self):
        return ', '.join([str(item) for item in self.services.all()])

    def get_salons(self):
        return ', '.join([str(item) for item in self.salons.all()])

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"


class Salon(models.Model):
    address = models.CharField(max_length=100, verbose_name='Адрес салона')

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "Салон"
        verbose_name_plural = "Салоны"


class Registration(models.Model):
    salon = models.ForeignKey(Salon, verbose_name='Салон', on_delete=models.CASCADE)
    master = models.ForeignKey(Master, verbose_name='Мастер', on_delete=models.CASCADE)
    client = models.ForeignKey(Client, verbose_name='Клиент', on_delete=models.CASCADE)
    service = models.ForeignKey(Service, verbose_name='Услуга', on_delete=models.CASCADE)
    time_registration = models.DateTimeField(auto_now_add=True, verbose_name='Время регистрации')
    reminder_sent = models.BooleanField(default=False, verbose_name='Отправилось напоминание')

    def __str__(self):
        return f"Заказ №{self.pk}"

    class Meta:
        verbose_name = "Забронированный заказ"
        verbose_name_plural = "Забронированные заказы"
