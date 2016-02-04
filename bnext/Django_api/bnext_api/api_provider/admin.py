from django.contrib import admin
from .models import Article, Comment, SubComment

class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title', 'category')

	list_filter = ['category']

admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(SubComment)
