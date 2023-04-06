from django.contrib import admin

from checkins import models


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["id", "question"]
    list_display_links = ["id", "question"]


class AnswerInline(admin.TabularInline):
    model = models.Answer
    extra = 0


@admin.register(models.Checkin)
class CheckinAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "created_at"]
    list_display_links = ["id", "user", "created_at"]
    # readonly_fields = ["created_at"]
    inlines = [AnswerInline]


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "question"]

    def get_user(self, instance):
        print(instance)


@admin.register(models.Feeling)
class FeelingAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": ["user", "choice", "created_at"],
            },
        ),

    ]


admin.site.register(models.FeelingType)
