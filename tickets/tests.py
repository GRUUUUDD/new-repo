from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import CustomUser
from .models import Ticket


class TicketsTestCase(TestCase):
    def setUp(self):
        # Создаем тестовых пользователей
        self.resident = CustomUser.objects.create_user(
            username="resident",
            password="testpass123",
            role=3  # Жилец
        )

        self.specialist = CustomUser.objects.create_user(
            username="plumber",
            password="testpass123",
            role=4  # Сантехник
        )

        self.tszh_member = CustomUser.objects.create_user(
            username="tszh_member",
            password="testpass123",
            role=2  # Член ТСЖ
        )

        # Создаем тестовую заявку
        self.ticket = Ticket.objects.create(
            author=self.resident,
            receiver=self.tszh_member,
            description="Протекает кран",
            status="open"
        )

        # Клиент для имитации запросов
        self.client = Client()

    # Тест 1: Жилец может создать заявку
    def test_resident_can_create_ticket(self):
        self.client.login(username="resident", password="testpass123")
        response = self.client.post(reverse('tickets:create'), {
            'receiver': self.tszh_member.id,
            'description': 'Сломался лифт',
        })
        self.assertEqual(response.status_code, 302)  # Проверяем перенаправление
        self.assertEqual(Ticket.objects.count(), 2)  # Заявка добавилась

    # Тест 2: Получатель может изменить статус
    def test_receiver_can_update_status(self):
        self.client.login(username="tszh_member", password="testpass123")
        response = self.client.get(reverse('tickets:update_status', args=[self.ticket.id, 'accepted']))
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, 'accepted')

    # Тест 3: Детальный просмотр заявки
    def test_ticket_detail_view(self):
        self.client.login(username="tszh_member", password="testpass123")
        response = self.client.get(reverse('tickets:detail', args=[self.ticket.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Протекает кран")  # Проверяем описание

    # Тест 4: История заявок для жильца
    def test_resident_history(self):
        self.client.login(username="resident", password="testpass123")
        response = self.client.get(reverse('tickets:history'))
        self.assertEqual(len(response.context['tickets']), 1)  # Видит 1 заявку

    # Тест 5: История заявок для ТСЖ
    def test_tszh_history(self):
        self.client.login(username="tszh_member", password="testpass123")
        response = self.client.get(reverse('tickets:history'))
        self.assertEqual(len(response.context['tickets']), 1)  # Видит входящую заявку