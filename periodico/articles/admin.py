from django.contrib import admin
from .models import Article, Comment


class CommentInline(admin.TabularInline):  # new
    model = Comment


class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]

#Registramos el modelo Article, e indicamos que se use un módulo administrativo que hemos tuneado para incluir los inlines
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
