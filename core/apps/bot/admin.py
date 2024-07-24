from django.contrib import admin

from .models import Question, Salon


class FlatAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_editable = ('name',)


admin.site.register(Question)

admin.site.register(Salon)