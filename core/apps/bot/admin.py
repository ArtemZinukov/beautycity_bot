from django.contrib import admin

from .models import Client, Salon, Service, Registration, Master


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone')
    search_fields = ('username', 'phone')
    list_filter = ('username', 'phone')


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    search_fields = ('name', )
    list_display = ["name", "get_services", "get_salons"]


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    search_fields = ('title', )
    list_display = ["title", "price"]


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('client', 'master', 'salon', 'service', 'time_registration')
    list_filter = ('salon', 'master', 'client', 'service')
    search_fields = ('salon__name', 'master__name', 'client__name', 'service__name')
    readonly_fields = ('time_registration',)


admin.site.register(Salon)



