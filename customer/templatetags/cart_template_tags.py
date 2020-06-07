from django import template
from customer.models import Order

register = template.Library()


@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        try:
                order  = Order.objects.get(customer=user.customer, complete=False)
                items = order.orderitem_set.all()
        except:
                items = []
        if items:
                if items.exists():
                        return items.count()
    return 0