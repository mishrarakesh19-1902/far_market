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
