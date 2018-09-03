from django.utils.dateparse import parse_date


def format_product_price(price_in_cents):
    return '${0:.2f}'.format(price_in_cents / 100)


def parse_date_str(date_str):
    try:
        date = parse_date(date_str)
    except ValueError:
        return None
    return date
