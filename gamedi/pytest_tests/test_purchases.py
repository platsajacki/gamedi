import pytest
from pytest_lazyfixture import lazy_fixture as lf

from http import HTTPStatus
from uuid import UUID
from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse
from django.test import Client, RequestFactory
from django.urls import reverse

from games.models import Game
from purchases.models import Purchase
from purchases.services import ConfirmationService, CreatePurchaseService
from users.models import User

pytestmark = pytest.mark.django_db


class TestPurchaseRoutes:
    """Тесты urls для покупок."""
    def test_purchase_owner_cannot_payment(self, owner_client: Client, game_slug: tuple[str]):
        """Владелец игры не может перейти на страницу оплаты повторно."""
        assert owner_client.get(reverse('purchases:payment', args=game_slug)).status_code == HTTPStatus.FORBIDDEN

    def test_anonymous_redirected_to_login_for_payment(self, client: Client, game_slug: tuple[str]):
        """Анонимного пользователя перенаправляет на регистрацию при переходе на покупку."""
        response = client.get(reverse('purchases:payment', args=game_slug))
        assert response.status_code == HTTPStatus.FOUND
        assert 'login' in response.url  # type: ignore[attr-defined]

    def test_authenticated_user_redirected_to_payment_page(self, user_client: Client, game_slug: tuple[str]):
        """Пользователь без данной игры перенаправляется на страницу оплаты."""
        response = user_client.get(reverse('purchases:payment', args=game_slug))
        assert response.status_code == HTTPStatus.FOUND
        assert 'yoomoney.ru' in response.url   # type: ignore[attr-defined]

    @pytest.mark.parametrize(
        'visitor, status',
        [
            (lf('client'), HTTPStatus.OK),
            (lf('owner_client'), HTTPStatus.FORBIDDEN),
            (lf('user_client'), HTTPStatus.FORBIDDEN),
        ]
    )
    def test_confirmation_route(self, visitor: Client, status: int):
        """Только аноним может отправить POST запрос."""
        with patch('purchases.views.ConfirmationView.post') as mock_service:
            mock_service.return_value = HttpResponse({})
            assert visitor.post(reverse('purchases:confirmation')).status_code == status


class TestServicePurchase:
    """Проверка создания платежа."""
    @pytest.mark.parametrize(
        'visitor, status',
        [(AnonymousUser(), HTTPStatus.NOT_FOUND), (lf('owner'), HTTPStatus.NOT_FOUND), (lf('user'), HTTPStatus.FOUND)]
    )
    def test_service_create_payment(self, visitor: User | AnonymousUser, status: int, game_slug: tuple[str]):
        """Проверяет возможность создания платежа."""
        request: HttpRequest = RequestFactory().get(reverse('purchases:payment', args=game_slug))
        request.user = visitor
        kwargs: dict = {'slug': game_slug[0]}
        assert CreatePurchaseService(request=request, kwargs=kwargs)().status_code == status

    @pytest.mark.parametrize('visitor', [lf('owner'), lf('user')])
    def test_service_confirmation_valide_data_authorized_users(
        self, visitor: User | AnonymousUser, game: Game, user: User, yookassa_valide_data: dict, uuid_str: str,
    ):
        """Проверка сервиса подтверждения. Запрос с валидными данными от авторизованных пользователей."""
        request: HttpRequest = RequestFactory().post(
            reverse('purchases:confirmation'), data=yookassa_valide_data, content_type='application/json'
        )
        request.user = visitor
        Purchase.objects.create(
            idempotence_key=uuid_str, user=user, game=game, price=game.final_price  # type: ignore[misc]
        )
        with patch('yookassa.Payment.find_one') as mock_find_one:
            mock_find_one.return_value = HttpResponse({})
            assert ConfirmationService(request=request)().status_code == HTTPStatus.NOT_FOUND

    def test_service_confirmation_valide_data_anonymous(
        self, game: Game, user: User, yookassa_valide_data: dict, uuid_str: str
    ):
        """Проверка сервиса подтверждения. Запрос с валидными данными от анонима."""
        request: HttpRequest = RequestFactory().post(
            reverse('purchases:confirmation'), data=yookassa_valide_data, content_type='application/json'
        )
        request.user = AnonymousUser()
        Purchase.objects.create(
            idempotence_key=uuid_str, user=user, game=game, price=game.final_price  # type: ignore[misc]
        )
        with patch('yookassa.Payment.find_one') as mock_find_one:
            mock_find_one.return_value = HttpResponse({})
            assert ConfirmationService(request=request)().status_code == HTTPStatus.OK
        purchase: Purchase = Purchase.objects.get(idempotence_key=uuid_str)
        assert purchase.payment_id == UUID(yookassa_valide_data['object']['id'])
        assert purchase.status == yookassa_valide_data['object']['status']
        if purchase.status == 'succeeded':
            assert int(purchase.income_without_tax) == int(yookassa_valide_data['object']['income_amount']['value'])
            assert game in purchase.user.games.all()

    def test_service_confirmation_invalid_payment_id_anonymous(
        self, game: Game, user: User, yookassa_valide_data: dict, uuid_str: str
    ):
        """Проверка сервиса подтверждения. Запрос с неверным payment_id от анонима."""
        request: HttpRequest = RequestFactory().post(
            reverse('purchases:confirmation'), data=yookassa_valide_data, content_type='application/json'
        )
        request.user = AnonymousUser()
        Purchase.objects.create(
            idempotence_key=uuid_str, user=user, game=game, price=game.final_price  # type: ignore[misc]
        )
        CreatePurchaseService.set_configuration(self)  # type: ignore[arg-type]
        assert ConfirmationService(request=request)().status_code == HTTPStatus.NOT_FOUND
        purchase: Purchase = Purchase.objects.get(idempotence_key=uuid_str)
        assert purchase.payment_id is None
        assert purchase.status == 'pending'
        assert purchase.income_without_tax == 0
        assert not purchase.user.games.exists()

    def test_service_confirmation_invalid_object_anonymous(
        self, game: Game, user: User, yookassa_valide_data: dict, uuid_str: str
    ):
        """Проверка сервиса подтверждения. Запрос без object от анонима."""
        del yookassa_valide_data['object']
        request: HttpRequest = RequestFactory().post(
            reverse('purchases:confirmation'), data=yookassa_valide_data, content_type='application/json'
        )
        request.user = AnonymousUser()
        Purchase.objects.create(
            idempotence_key=uuid_str, user=user, game=game, price=game.final_price  # type: ignore[misc]
        )
        with patch('yookassa.Payment.find_one') as mock_find_one:
            mock_find_one.return_value = HttpResponse({})
            assert ConfirmationService(request=request)().status_code == HTTPStatus.NOT_FOUND
        purchase: Purchase = Purchase.objects.get(idempotence_key=uuid_str)
        assert purchase.payment_id is None
        assert purchase.status == 'pending'
        assert purchase.income_without_tax == 0
        assert not purchase.user.games.exists()

    @pytest.mark.parametrize('key', ['id', 'metadata', 'status', 'income_amount'])
    def test_service_confirmation_invalid_objects_key_anonymous(
        self, game: Game, user: User, yookassa_valide_data_succeeded: dict, uuid_str: str, key: str
    ):
        """Проверка сервиса подтверждения. Запрос с невалидными данными от анонима."""
        del yookassa_valide_data_succeeded['object'][key]
        request: HttpRequest = RequestFactory().post(
            reverse('purchases:confirmation'), data=yookassa_valide_data_succeeded, content_type='application/json'
        )
        request.user = AnonymousUser()
        Purchase.objects.create(
            idempotence_key=uuid_str, user=user, game=game, price=game.final_price  # type: ignore[misc]
        )
        with patch('yookassa.Payment.find_one') as mock_find_one:
            mock_find_one.return_value = HttpResponse({})
            assert ConfirmationService(request=request)().status_code == HTTPStatus.NOT_FOUND
        purchase: Purchase = Purchase.objects.get(idempotence_key=uuid_str)
        assert purchase.payment_id is None
        assert purchase.status == 'pending'
        assert purchase.income_without_tax == 0
        assert not purchase.user.games.exists()
