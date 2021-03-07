from django.contrib import admin

from .models import User, TeamLeaderModel, JudgeModel

# Register your models here.

admin.site.register(User)
admin.site.register(TeamLeaderModel)
admin.site.register(JudgeModel)
