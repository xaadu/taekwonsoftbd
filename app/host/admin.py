from django.contrib import admin

from .models import Event, Category, RegisteredTeam, RegisteredPlayer

# Register your models here.
admin.site.register(Event)
admin.site.register(Category)
admin.site.register(RegisteredTeam)
admin.site.register(RegisteredPlayer)
