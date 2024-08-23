import requests
import stripe
from rest_framework import status

from config.settings import CURRENCY_API_KEY, CURRENCY_API_URL, STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def convert_rub_to_dollars(rub_price):
    """Конвертирует рубли в доллары."""
    usd_price = 0
    response = requests.get(
        f"{CURRENCY_API_URL}v3/latest?apikey={CURRENCY_API_KEY}&currencies=RUB"
    )
    if response.status_code == status.HTTP_200_OK:
        usd_rate = response.json()["data"]["RUB"]["value"]
        usd_price = float(rub_price) / usd_rate
        return int(usd_price * 100)


def create_stripe_product():
    """Создает продукт в stripe."""
    product = stripe.Product.create(name="Stripe product")
    return product


def create_stripe_price(amount, product):
    """Создает цену в stripe."""

    return stripe.Price.create(
        currency="usd",
        unit_amount=amount,
        product=product.id,
    )


def create_stripe_session(price):
    """Создает сессию на оплату в stripe."""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def retrieve_stripe_session(session_id):
    """Получает данные о сессии в stripe по её идентификатору."""
    session = stripe.checkout.Session.retrieve(session_id)
    return session
