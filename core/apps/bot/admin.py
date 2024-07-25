from django.contrib import admin

from .models import Client, Salon, Service, Registration, Master

admin.site.register(Client)

admin.site.register(Salon)

admin.site.register(Service)

admin.site.register(Registration)

admin.site.register(Master)
