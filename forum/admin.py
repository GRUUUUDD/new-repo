from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_link', 'created_at')
    list_filter = ('created_at', 'author__role')
    search_fields = ('title', 'content')
    readonly_fields = ('preview_image',)

    def author_link(self, obj):
        return format_html('<a href="/admin/users/customuser/{}/change/">{}</a>',
                         obj.author.id, obj.author)
    author_link.short_description = 'Автор'

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="150" />', obj.image.url)
        return "-"
    preview_image.short_description = 'Превью'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('short_content', 'post_link', 'author_apartment', 'created_at', 'is_approved')
    list_filter = ('is_approved', 'created_at')
    list_editable = ('is_approved',)
    search_fields = ('content', 'author__apartment')

    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Комментарий'

    def post_link(self, obj):
        return format_html('<a href="/admin/forum/post/{}/change/">{}</a>',
                         obj.post.id, obj.post.title)
    post_link.short_description = 'Пост'

    def author_apartment(self, obj):
        return obj.author.apartment
    author_apartment.short_description = 'Квартира'
