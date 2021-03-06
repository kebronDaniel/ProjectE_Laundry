from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Item,Order,OrderItem,ShippingAddress
from django.views.generic import ListView,DetailView,View
from django.shortcuts import redirect
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm

@login_required
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

@login_required
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
            return redirect("order-summary-view")
        else:
            order.items.add(order_item)
            messages.info(request,"This Item was added to the cart")
            return redirect("order-summary-view")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user = request.user, ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request, "This New Item was added to the cart")
        return redirect("order-summary-view")

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(item = item, user= request.user, ordered = False)[0]
            order.items.remove(order_item)
            messages.info(request,"This Item was removed from your cart")
            return redirect("order-summary-view")
        else:
            messages.info(request,"This item was not in your cart")
            return redirect("item", slug=slug)

    else:
        messages.info(request,"You don't have an active order")
        return redirect("item", slug=slug)

    return redirect("item", slug=slug)

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]

        if order.items.filter(item__slug = item.slug).exists():
            order_item = OrderItem.objects.filter(item = item, user= request.user, ordered = False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request,"This Item Quantity is Updated.")
            return redirect("order-summary-view")
        else:
            messages.info(request,"This item was not in your cart")
            return redirect("item", slug=slug)

    else:
        messages.info(request,"You don't have an active order")
        return redirect("item", slug=slug)

    return redirect("item", slug=slug)



class OrderSummaryView(LoginRequiredMixin,View):
    def get(self, *args ,**kwargs):
        try:
            order = Order.objects.get(user = self.request.user, ordered = False)
            context = {
                'object': order
            }
            return render(self.request,'order_summary.html',context)
        except ObjectDoesNotExist:
            messages.error(self.request,"You don't have an active order")
            return redirect('/')

class CheckoutView(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            'form':form
        }
        return render(self.request,"checkout-page.html",context)
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user = self.request.user, ordered = False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                unique_name = form.cleaned_data.get('unique_name')
                phone = form.cleaned_data.get('phone')

                shipping_address = ShippingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    unique_name=unique_name,
                    phone=phone

                )
                shipping_address.save()
                return redirect("checkout")
            messages.warning(self.request,"Failed checkout")
            return redirect("checkout")
        except ObjectDoesNotExist:
            messages.error(self.request,"You don't have an active order")
            return redirect('order-summary')


