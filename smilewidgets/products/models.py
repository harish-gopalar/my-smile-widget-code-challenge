from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=25, help_text='Customer facing name of product')
    code = models.CharField(max_length=10, help_text='Internal facing reference to product')
    price = models.PositiveIntegerField(help_text='Price of product in cents')
    
    def __str__(self):
        return '{} - {}'.format(self.name, self.code)


class GiftCard(models.Model):
    code = models.CharField(max_length=30)
    amount = models.PositiveIntegerField(help_text='Value of gift card in cents')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return '{} - {}'.format(self.code, self.formatted_amount)
    
    @property
    def formatted_amount(self):
        return '${0:.2f}'.format(self.amount / 100)


# Newly Added

class ProductPrice(models.Model):
    name = models.CharField(max_length=64, help_text='Price Schedule Name')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    date_start = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    price = models.PositiveIntegerField(default=0, help_text='Price of the product in cents')
    is_blackfriday = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {}'.format(self.product_id.name, self.name)


# This class created just because, not to make hard code the dates

class BlackFriday(models.Model):
    date = models.DateField()

    def __str__(self):
        return str(self.date)

