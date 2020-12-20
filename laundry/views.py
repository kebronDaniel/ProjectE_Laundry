from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Item,Order,OrderItem
from django.views.generic import ListView,DetailView
from django.shortcuts import redirect
from django.utils import timezone

def checkout(request):
    context = {
        "items": Item.objects.all()
    }
    return render(request, 'checkout-page.html', context)

class HomeView(ListView):
    model = Item
    paginate_by = 3
    template_name = "home-page.html"

class ItemDetailView(DetailView):
    model = Item
    template_name = "product-page.html"

def add_to_cart(request,slug):

    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(item = item, user = request.user, ordered = False)
    order_qs = Order.objects.filter(user = request.user, ordered = False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug = item.slug).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request,"Item qunatity is updated!")
            return redirect("item", slug=slug)
        else:
            order.items.add(order_item)
            messages.info(request,"This Item was added to the cart")
            return redirect("item", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user, ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request, "This New Item was added to the cart")
        return redirect("item", slug=slug)

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(item = item, user= request.user, ordered = False)[0]
            order.items.remove(order_item)
            messages.info(request,"This Item was removed from your cart")
            return redirect("item", slug=slug)
        else:
            messages.info(request,"This item was not in your cart")
            return redirect("item", slug=slug)

    else:
        messages.info(request,"You don't have an active order")
        return redirect("item", slug=slug)

    return redirect("item", slug=slug)