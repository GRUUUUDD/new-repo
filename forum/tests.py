from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from users.models import CustomUser
from .models import Post, Comment
from .utils import check_profanity


class ForumTests(TestCase):
    def setUp(self):
        # Создаем тестовых пользователей
        self.tszh_user = CustomUser.objects.create_user(
            username="tszh_user",
            password="testpass123",
            role=2,  # Член ТСЖ
            apartment="101"
        )

        self.resident_user = CustomUser.objects.create_user(
            username="resident",
            password="testpass123",
            role=3,  # Жилец
            apartment="102"
        )

        # Тестовый пост
        self.post = Post.objects.create(
            author=self.tszh_user,
            title="Ремонт лифта",
            content="Запланирован на среду"
        )

        # Тестовые комментарии
        self.comment1 = Comment.objects.create(
            post=self.post,
            author=self.resident_user,
            content="Спасибо за информацию!",
            is_approved=True
        )

        self.comment2 = Comment.objects.create(
            post=self.post,
            author=self.resident_user,
            content="Где подробности, блять?",
            is_approved=False
        )

        self.client = Client()

    # Тест 1: Только члены ТСЖ могут создавать посты
    def test_tszh_post_creation(self):
        # Логиним члена ТСЖ
        self.client.login(username="tszh_user", password="testpass123")
        response = self.client.post(reverse('create_post'), {
            'title': 'Уборка территории',
            'content': 'Просим соблюдать чистоту'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.count(), 2)

    def test_resident_cant_create_post(self):
        # Логиним обычного жильца
        self.client.login(username="resident", password="testpass123")
        response = self.client.get(reverse('create_post'))
        self.assertEqual(response.status_code, 403)

    # Тест 2: Фильтрация запрещенных слов в комментариях
    def test_profanity_filter(self):
        self.client.login(username="resident", password="testpass123")
        response = self.client.post(reverse('add_comment', args=[self.post.id]), {
            'content': 'Это пиздец какой-то!'
        })
        comment = Comment.objects.latest('id')
        self.assertFalse(comment.is_approved)

    # Тест 3: Отображение только одобренных комментариев
    def test_approved_comments_display(self):
        response = self.client.get(reverse('forum'))
        post = response.context['posts'].first()
        self.assertEqual(len(post.approved_comments), 1)
        self.assertNotIn(self.comment2, post.approved_comments)

    # Тест 4: Удаление поста доступно только ТСЖ
    def test_post_deletion_permissions(self):
        # Попытка удалить пост жильцом
        self.client.login(username="resident", password="testpass123")
        response = self.client.post(reverse('delete_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 403)

        # Удаление постa членом ТСЖ
        self.client.login(username="tszh_user", password="testpass123")
        response = self.client.post(reverse('delete_post', args=[self.post.id]))
        self.assertEqual(Post.objects.count(), 0)