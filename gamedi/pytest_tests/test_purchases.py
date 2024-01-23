import pytest
# from pytest_lazyfixture import lazy_fixture as lf

from http import HTTPStatus

from django.test.client import Client
from django.urls import reverse

pytestmark = pytest.mark.django_db


class TestPurchaseRoutes:
    """Тесты urls для покупок."""
    def test_purchase_owner_can_not_payment(self, owner_client: Client, game_slug: tuple[str]):
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
