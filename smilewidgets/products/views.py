from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, ProductPrice, GiftCard, BlackFriday
import datetime


@api_view(['POST', 'GET'])
def GetPrice(request):
    output_data = {'product_price': 0}

    requested_date = request.data.get('date', False)
    # requested_date = datetime.date.today()

    requested_date = datetime.datetime.strptime(requested_date, "%Y-%m-%d").date() if requested_date and type(requested_date) == str \
        else requested_date
    date = requested_date

    productCode = request.data.get('productCode', False)
    # productCode = 'big_widget'

    giftCardCode = request.data.get('giftCardCode', False)
    # giftCardCode = '10OFF'

    product_price = 0
    if productCode and date:
        product = Product.objects.get(code=productCode)
        product_price = product.price

        is_blackfriday = True if BlackFriday.objects.filter(date=date) else False
        if is_blackfriday:
            productprice_obj = ProductPrice.objects.filter(product_id=product, is_blackfriday=True)
            product_price = productprice_obj[0].price if productprice_obj else product_price
        else:
            productprice_obj = ProductPrice.objects.filter(product_id=product, is_blackfriday=False)
            product_price = productprice_obj[0].price \
                if productprice_obj and productprice_obj[0].date_start <= date else product_price

        ## If Gift Code exist
        if giftCardCode:
            giftCardCode_obj = GiftCard.objects.filter(code=giftCardCode)
            if giftCardCode_obj and giftCardCode_obj[0].date_end:
                gift_amount = giftCardCode_obj[0].amount if giftCardCode_obj and date <= giftCardCode_obj.date_start <= date  else 0
            else:
                gift_amount = giftCardCode_obj[0].amount if giftCardCode_obj and giftCardCode_obj[0].date_start <= date else 0
            if product_price > gift_amount:
                product_price = product_price - gift_amount
            else:
                product_price = 0

    output_data['product_price'] = product_price

    return Response(output_data)
