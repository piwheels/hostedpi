from hostedpi.settings import Settings


def test_settings():
    settings = Settings(
        id="test_id",
        secret="test_secret",
        auth_url="https://auth.mythic-beasts.com/login",
        api_url="https://api.mythic-beasts.com/beta/pi/",
    )
    assert settings.id == "test_id"
    assert settings.secret.get_secret_value() == "test_secret"
    assert str(settings.auth_url) == "https://auth.mythic-beasts.com/login"
    assert str(settings.api_url) == "https://api.mythic-beasts.com/beta/pi/"


def test_settings_with_api_url_without_trailing_slash():
    settings = Settings(
        id="test_id",
        secret="test_secret",
        auth_url="https://auth.mythic-beasts.com/login",
        api_url="https://api.mythic-beasts.com/beta/pi",
    )
    assert str(settings.api_url) == "https://api.mythic-beasts.com/beta/pi/"
