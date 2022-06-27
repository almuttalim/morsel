from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from .models import MenuItem, Category, OrderModel
from django.core.mail import send_mail

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')

class Order(View):
    def get(self, request, *args, **kwargs):
        #get every item from each category
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')
        mains = MenuItem.objects.filter(category__name__contains='Main')

    #pass into context
        context = {
            'appetizers': appetizers,
            'desserts': desserts,
            'drinks': drinks,
            'mains': mains,
        }   
    
    #render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):

        order_items = {
            'items':[]
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk=int(item))
            item_data = {
                'id': menu_item.pk,
                'name' : menu_item.name,
                'price' : menu_item.price,
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(price=price,
        name = request.POST.get('name'),
        email = request.POST.get('email'),
        street = request.POST.get('street'),
        city = request.POST.get('city'),
        state = request.POST.get('state'),
        zip_code = request.POST.get('zip')
        )
 
        email = request.POST.get('email')
        order.items.add(*item_ids)

        body = ('Thank You for your order! Your food is being prepared and will be delivered shortly.\n'
        f'Your total: {price}\n')

        #Send confirmation email after everthing is done
        send_mail(
            'Thank You for your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)

        


class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }

        return render(request, 'customer/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        print(request.body)

class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')

class Menu(View):
    def get(self, request, *args, **kwargs):
        menu_items = MenuItem.objects.all()

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)

class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")

        menu_items = MenuItem.objects.filter(
            Q(name__icontains=query) | 
            Q(price__icontains=query) | 
            Q(description__icontains=query)
        )

        context = {
            'menu_items': menu_items
        }

        return render(request, 'customer/menu.html', context)