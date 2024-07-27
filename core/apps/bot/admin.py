from django.contrib import admin

from .models import Client, Salon, Service, Registration, Master


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'username', 'phone_number')
    search_fields = ("tg_id", 'username', 'phone_number')
    list_filter = ('username', 'phone_number')


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
    list_display = ('client', 'master', 'salon', 'service', 'time_registration', 'reminder_sent', 'service_date')
    list_filter = ('salon', 'master', 'client', 'service', 'reminder_sent')
    search_fields = ('salon__name', 'master__name', 'client__name', 'service__name')
    readonly_fields = ('time_registration',)


admin.site.register(Salon)



