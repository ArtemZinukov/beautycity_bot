from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class Client(models.Model):
    username = models.CharField(max_length=50)


class Service(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=2, decimal_places=2)


class Master(models.Model):
    name = models.CharField(max_length=50)
    service = models.ForeignKey(Service)


class Salon(models.Model):
    adress = models.CharField(max_length=100)
    master = models.ForeignKey(Master)


class Registration(models.Model):
    salon = models.ForeignKey(Salon)
    master = models.ForeignKey(Master)
    client = models.ForeignKey(Client)
    service = models.ForeignKey(Service)
    time_registration = models.DateTimeField(auto_now=False, auto_now_add=False)