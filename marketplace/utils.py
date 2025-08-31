# marketplace/utils.py
from sklearn.linear_model import LinearRegression
import numpy as np

def predict_price(quantity):
    # Dummy data: quantity vs. price
    X = np.array([[10], [20], [30], [40], [50]])  # Quantities
    y = np.array([100, 150, 200, 250, 300])  # Prices

    model = LinearRegression()
    model.fit(X, y)

    predicted_price = model.predict([[quantity]])
    return predicted_price[0]

# marketplace/utils.py

from django.core.mail import send_mail
from django.conf import settings

def send_welcome_email(to_email, username):
    subject = "Welcome to Farm Market!"
    message = f"Hello {username},\n\nYour account has been created successfully.\nThank you for joining Farm Market!"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [to_email]

    send_mail(subject, message, from_email, recipient_list)
