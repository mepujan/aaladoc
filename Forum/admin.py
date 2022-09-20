from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Category)
class article(admin.ModelAdmin):
    list_display = ("title","written_by","date","no_comments","publish")
    search_fields = ("title","written_by","body")
    list_filter = ("date","publish")
    list_per_page = 20
admin.site.register(Article,article)

class articlecomments(admin.ModelAdmin):
    list_display = ("comment_by","comments","created")
    search_fields = ("comment_by","comments")
    list_per_page = 20

admin.site.register(ArticleComments,articlecomments)

class question(admin.ModelAdmin):
    list_display = ("question","asked_by","date","no_comments","verify")
    search_fields = ("question","asked_by")
    list_filter = ("date","verify")
    list_per_page = 20

admin.site.register(Question,question)
admin.site.register(QuestionComments)

admin.site.register(ArticleLiked)