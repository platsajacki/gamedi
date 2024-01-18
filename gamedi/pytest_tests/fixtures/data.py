import pytest

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def registration_data() -> dict[str, str]:
    """Возвращает словарь с регистрационными данными."""
    return {
        'username': 'test',
        'email': 'test@test.ru',
        'password1': 'first_test',
        'password2': 'first_test',
    }


@pytest.fixture
def temp_img_data() -> dict:
    return {
        'prefix': 'file',
        'suffix': '.png',
        'dir': settings.MEDIA_ROOT,
    }


@pytest.fixture
def image_data() -> dict:
    """Фикстура, возвращающая словарь с данными изображения."""
    return {
        'name': 'test_image.jpg',
        'content': open(f'{settings.BASE_DIR}/pytest_tests/image.png', 'rb').read(),
        'content_type': 'image/png',
    }


@pytest.fixture
def image_with_another_name(image_data: dict) -> SimpleUploadedFile:
    """Фикстура, возвращающая словарь с данными изображения."""
    image_data.update(name='test_image2.jpg')
    return SimpleUploadedFile(**image_data)
