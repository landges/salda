from .models import ProductInBasket


def getting_basket_info(request):

    session_key = request.session.session_key
    if not session_key:
        #workaround for newer Django versions
        request.session["session_key"] = 123
        #re-apply value
        request.session.cycle_key()
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True, order__isnull=True)
    products_in_basket_view=[t.product for t in products_in_basket]
    products_total_nmb = products_in_basket.count()
    total_amount=sum([item.total_price for item in products_in_basket])
    print('hello')
    sale=float(total_amount)*0.20
    return locals()