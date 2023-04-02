from django.contrib import admin

from checkins import models


admin.site.register([models.Question, models.Answer, models.Checkin])