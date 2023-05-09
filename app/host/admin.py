from django.contrib import admin

from .models import Event, Category, SubCategory, RegisteredTeam, RegisteredPlayer, PlayerResult

# Register your models here.
admin.site.register(Event)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(RegisteredTeam)
admin.site.register(RegisteredPlayer)
admin.site.register(PlayerResult)
