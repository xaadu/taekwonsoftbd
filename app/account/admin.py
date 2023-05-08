from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, TeamLeaderModel, JudgeModel

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(TeamLeaderModel)
admin.site.register(JudgeModel)
