from django.db import models
from django.db.models import Q


class Product(models.Model):
    name = models.CharField(max_length=25, help_text='Customer facing name of product')
    code = models.CharField(max_length=10, help_text='Internal facing reference to product')
    price = models.PositiveIntegerField(help_text='Price of product in cents')

    def get_season_price(self, date):
        season_product_price_obj = ProductPrice.objects.filter(
            Q(date_end__gte=date) | Q(date_end__isnull=True),
            date_start__lte=date,
            product=self
        ).order_by('price').first()

        if season_product_price_obj is not None:
            price = season_product_price_obj.price
        else:
            price = self.price
        return price

    def __str__(self):
        return '{} - {}'.format(self.name, self.code)


class GiftCard(models.Model):
    code = models.CharField(max_length=30)
    amount = models.PositiveIntegerField(help_text='Value of gift card in cents')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    def __str__(self):
        return '{} - {}'.format(self.code, self.formatted_amount)

    def is_active(self, date):
        if self.date_start <= date:
            if self.date_end is None:
                return True
            if self.date_end >= date:
                return True
        return False

    def apply(self, price):
        return max(0, price - self.amount)

    @property
    def formatted_amount(self):
        return '${0:.2f}'.format(self.amount / 100)


class ProductPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
