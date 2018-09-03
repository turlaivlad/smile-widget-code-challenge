from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from products.models import Product, GiftCard
from products.utils import format_product_price, parse_date_str


class ProductPriceAPIView(APIView):
    def get(self, request):
        product_code = request.query_params.get('productCode')
        date_str = request.query_params.get('date')
        gift_card_code = request.query_params.get('giftCardCode')

        if product_code is None:
            return Response({'error': 'Product code is required'}, status=status.HTTP_400_BAD_REQUEST)
        if date_str is None:
            return Response({'error': 'Date is required'}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, code=product_code)

        date = parse_date_str(date_str)
        if date is None:
            return Response({'error': 'Invalid date'}, status=status.HTTP_400_BAD_REQUEST)

        price = product.get_season_price(date)

        if gift_card_code is not None:
            try:
                gift_card = GiftCard.objects.get(code=gift_card_code)
            except GiftCard.DoesNotExist:
                return Response({'error': 'Invalid gift code'}, status=status.HTTP_400_BAD_REQUEST)
            if gift_card.is_active(date):
                price = gift_card.apply(price)

        return Response({'price': format_product_price(price)})
