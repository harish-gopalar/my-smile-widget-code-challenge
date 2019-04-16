from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, ProductPrice, GiftCard, BlackFriday
import datetime


@api_view(['POST', 'GET'])
def get_price_details(request):
    response_data = {'product_price': 0}

    requested_date = request.data.get('date', False)

    requested_date = datetime.datetime.strptime(requested_date, "%Y-%m-%d").date() \
        if requested_date and type(requested_date) == str else requested_date
    date = requested_date

    product_code = request.data.get('productCode', False)

    gift_card_code = request.data.get('giftCardCode', False)

    product_price = 0
    if product_code and date:
        product = Product.objects.get(code=product_code)
        product_price = product.price

        is_blackfriday = True if BlackFriday.objects.filter(date=date) else False
        if is_blackfriday:
            productprice_obj = ProductPrice.objects.filter(product_id=product, is_blackfriday=True)
            product_price = productprice_obj[0].price if productprice_obj else product_price
        else:
            productprice_obj = ProductPrice.objects.filter(product_id=product, is_blackfriday=False)
            product_price = productprice_obj[0].price \
                if productprice_obj and productprice_obj[0].date_start <= date else product_price

        # If Gift Code exist #
        if gift_card_code:
            gift_card_code_obj = GiftCard.objects.filter(code=gift_card_code)
            if gift_card_code_obj and gift_card_code_obj[0].date_end:
                gift_amount = gift_card_code_obj[0].amount if gift_card_code_obj \
                                                              and date <= gift_card_code_obj.date_start <= date else 0
            else:
                gift_amount = gift_card_code_obj[0].amount if gift_card_code_obj and \
                                                              gift_card_code_obj[0].date_start <= date else 0
            if product_price > gift_amount:
                product_price = product_price - gift_amount
            else:
                product_price = 0

    response_data['product_price'] = product_price

    return Response(response_data)
