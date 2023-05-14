from django.contrib import admin

from .models import Event, Category, SubCategory, RegisteredTeam, RegisteredPlayer, RegisteredMember, PlayerResult

# Register your models here.

@admin.register(RegisteredMember)
class RegisteredMemberAdmin(admin.ModelAdmin):
    pass


admin.site.register(Event)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(RegisteredTeam)
admin.site.register(RegisteredPlayer)
# admin.site.register(RegisteredMember)
admin.site.register(PlayerResult)
