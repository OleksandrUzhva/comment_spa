from typing import Dict
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


def generate_captcha() -> Dict[str, str]:
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    return {"hashkey": hashkey, "image_url": image_url}


def validate_captcha(hashkey: str, user_value: str) -> bool:
    if not hashkey or not user_value:
        return False

    try:
        store = CaptchaStore.objects.get(hashkey=hashkey)
    except CaptchaStore.DoesNotExist:
        return False

    is_valid = (store.response or "").lower() == user_value.strip().lower()

    store.delete()
    return is_valid