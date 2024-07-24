from django.db import models


class Client(models.Model):
    username = models.CharField(max_length=50)


class Service(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=2, decimal_places=2)


class Master(models.Model):
    name = models.CharField(max_length=50)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)


class Salon(models.Model):
    adress = models.CharField(max_length=100)
    master = models.ForeignKey(Master, on_delete=models.CASCADE)


class Registration(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE)
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    time_registration = models.DateTimeField(auto_now=False, auto_now_add=False)
    