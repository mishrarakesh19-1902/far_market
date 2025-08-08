# marketplace/management/commands/update_prices.py
from django.core.management.base import BaseCommand
from marketplace.models import Crop
from marketplace.utils import predict_price

class Command(BaseCommand):
    help = 'Update crop prices based on AI predictions'

    def handle(self, *args, **kwargs):
        # Get all crops from the database
        crops = Crop.objects.all()

        # Loop through each crop and update its price
        for crop in crops:
            predicted_price = predict_price(crop.quantity)  # Predict price based on quantity
            crop.price = predicted_price  # Update the price field with the predicted price
            crop.save()  # Save the updated crop object

        self.stdout.write(self.style.SUCCESS('Successfully updated crop prices!'))
