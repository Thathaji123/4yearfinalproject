from django.db import models

class Product(models.Model):
    item_name = models.CharField(max_length=100)
    price = models.FloatField()
    holding_cost = models.FloatField()
    ordering_cost = models.FloatField()
    quantity = models.IntegerField()
    predicted_sales = models.FloatField(blank=True, null=True)
    eoq = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.item_name
    

from django.http import JsonResponse
from .models import Product

def graph_data(request):
    products = Product.objects.all()
    product_names = [product.item_name for product in products]
    product_quantities = [product.quantity for product in products]
    eoq_thresholds = [int(product.eoq * 0.2) for product in products]  # 20% of EOQ

    return JsonResponse({
        'product_names': product_names,
        'product_quantities': product_quantities,
        'eoq_thresholds': eoq_thresholds,  # Include thresholds in the response
    })