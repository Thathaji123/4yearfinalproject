


from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

# Home view to take user input


def start(request):
    return render(request,'start.html')
def home(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        price = float(request.POST.get('price'))
        holding_cost = float(request.POST.get('holding_cost'))
        ordering_cost = float(request.POST.get('ordering_cost'))
        quantity = int(request.POST.get('quantity'))

        # Simulate realistic sales data based on price
        if price > 10000:  # High-priced item (e.g., mobile phone)
            sales_data = np.array([2, 3, 4, 3, 2])
        else:  # Low-priced item (e.g., notebook)
            sales_data = np.array([20, 25, 30, 25, 20])

        # Train ARIMA model
        model = ARIMA(sales_data, order=(1, 1, 1))
        model_fit = model.fit()
        predicted_sales = model_fit.forecast(steps=1)[0]

        # Apply scaling and convert to integer
        scaling_factor = 0.8
        predicted_sales = int(predicted_sales * scaling_factor)

        # Ensure predicted sales are within realistic limits
        if price > 10000:
            predicted_sales = min(predicted_sales, 5)
        else:
            predicted_sales = min(predicted_sales, 50)

        # Calculate EOQ
        demand = predicted_sales * 30  # Monthly demand (assuming 30 days)
        eoq = np.sqrt((2 * demand * ordering_cost) / holding_cost)
        eoq = int(eoq)

        # Save to database
        product = Product(
            item_name=item_name,
            price=price,
            holding_cost=holding_cost,
            ordering_cost=ordering_cost,
            quantity=quantity,
            predicted_sales=predicted_sales,
            eoq=eoq
        )
        product.save()

    # Fetch all products to display on the home page
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


# Product detail view
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})


# Delete product view
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('home')
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        product.item_name = request.POST.get('item_name')
        product.price = float(request.POST.get('price'))
        product.holding_cost = float(request.POST.get('holding_cost'))
        product.ordering_cost = float(request.POST.get('ordering_cost'))
        product.quantity = int(request.POST.get('quantity'))
        product.save()
        return redirect('product_detail', product_id=product.id)
    
    return render(request, 'edit_product.html', {'product': product})

# def home(request):
#     if request.method == 'POST':
#         item_name = request.POST.get('item_name')
#         price = float(request.POST.get('price'))
#         holding_cost = float(request.POST.get('holding_cost'))
#         ordering_cost = float(request.POST.get('ordering_cost'))
#         quantity = int(request.POST.get('quantity'))

#         # Simulate realistic sales data based on price
#         if price > 10000:  # High-priced item (e.g., mobile phone)
#             sales_data = np.array([2, 3, 4, 3, 2])  # Simulated daily sales (1–5 units)
#         else:  # Low-priced item (e.g., notebook)
#             sales_data = np.array([20, 25, 30, 25, 20])  # Simulated daily sales (20–50 units)

#         # Train ARIMA model
#         model = ARIMA(sales_data, order=(1, 1, 1))
#         model_fit = model.fit()
#         predicted_sales = model_fit.forecast(steps=1)[0]

#         # Apply a scaling factor to reduce predicted sales
#         scaling_factor = 0.8  # Reduce predictions by 20%
#         predicted_sales = predicted_sales * scaling_factor

#         # Ensure predicted sales are realistic
#         if price > 10000:  # High-priced item
#             predicted_sales = min(predicted_sales, 5)  # Max 5 units per day
#         else:  # Low-priced item
#             predicted_sales = min(predicted_sales, 50)  # Max 50 units per day

#         # Calculate EOQ
#         demand = predicted_sales * 30  # Monthly demand (assuming 30 days)
#         eoq = np.sqrt((2 * demand * ordering_cost) / holding_cost)

#         # Convert EOQ to an integer
#         eoq = int(eoq)  # Ensure EOQ is an integer

#         # Save to database
#         product = Product(
#             item_name=item_name,
#             price=price,
#             holding_cost=holding_cost,
#             ordering_cost=ordering_cost,
#             quantity=quantity,
#             predicted_sales=predicted_sales,
#             eoq=eoq  # Save EOQ as an integer
#         )
#         product.save()

#     # Fetch all products to display on the home page
#     products = Product.objects.all()
#     return render(request, 'home.html', {'products': products})

# # Product detail view
# def product_detail(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     return render(request, 'product_detail.html', {'product': product})

# # Delete product view
# def delete_product(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     product.delete()
#     return redirect('home')



# from django.shortcuts import render
# from .models import Product
# import json



# def product_graph(request):
#     products = Product.objects.all()
    
#     # Prepare data for Chart.js
#     product_names = [product.item_name for product in products]
#     product_quantities = [product.quantity for product in products]
#     low_quantity_thresholds = [int(product.quantity * 0.4) for product in products]  # 40% of actual quantity

#     # Pass data to template as JSON
#     context = {
#         'product_names': json.dumps(product_names),
#         'product_quantities': json.dumps(product_quantities),
#         'low_quantity_thresholds': json.dumps(low_quantity_thresholds),  # Pass thresholds to the template
#     }
    
#     return render(request, 'graph.html', context)


from django.shortcuts import render
from .models import Product
import json

def product_graph(request):
    products = Product.objects.all()
    
    # Prepare data for Chart.js
    product_names = [product.item_name for product in products]
    product_quantities = [product.quantity for product in products]
    low_quantity_thresholds = [int(product.quantity * 0.4) for product in products]  # 40% of actual quantity

    # Pass data to template as JSON
    context = {
        'product_names': json.dumps(product_names),
        'product_quantities': json.dumps(product_quantities),
        'low_quantity_thresholds': json.dumps(low_quantity_thresholds),  # Pass thresholds to the template
    }
    
    return render(request, 'graph.html', context)
# # Graph view to display product quantity in a bar chart
# def product_graph(request):
#     products = Product.objects.all()
    
#     # Prepare data for Chart.js
#     product_names = [product.item_name for product in products]
#     product_quantities = [product.quantity for product in products]
#     eoq_thresholds = [int(product.eoq * 0.2) for product in products]  # 20% of EOQ

#     # Pass data to template as JSON
#     context = {
#         'product_names': json.dumps(product_names),
#         'product_quantities': json.dumps(product_quantities),
#         'eoq_thresholds': json.dumps(eoq_thresholds),  # Pass thresholds to the template
#     }
    
#     return render(request, 'graph.html', context)


# def shop(request):
#     products = Product.objects.all()
#     return render(request, 'shop.html', {'products': products})


from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from .models import Product

def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})

def buy_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if product.quantity > 0:
        product.quantity -= 1  # Reduce quantity by 1
        product.save()

        # Check if quantity is below 20
        if product.quantity < 20:
            messages.warning(request, f"Warning: {product.item_name} quantity is below 20!")

        # Delete product if quantity reaches 0
        if product.quantity == 0:
            product.delete()
            return JsonResponse({
                'status': 'success',
                'message': f"{product.item_name} is out of stock and has been removed.",
                'deleted': True,
                'product_name': product.item_name,
                'quantity': 0
            })

        return JsonResponse({
            'status': 'success',
            'message': f"{product.item_name} quantity updated.",
            'deleted': False,
            'product_name': product.item_name,
            'quantity': product.quantity
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': f"{product.item_name} is already out of stock."
        }, status=400)

def product_graph(request):
    products = Product.objects.all()
    product_names = [product.item_name for product in products]
    product_quantities = [product.quantity for product in products]
    return render(request, 'graph.html', {
        'product_names': json.dumps(product_names),
        'product_quantities': json.dumps(product_quantities),
    })

def graph_data(request):
    products = Product.objects.all()
    product_names = [product.item_name for product in products]
    product_quantities = [product.quantity for product in products]
    return JsonResponse({
        'product_names': product_names,
        'product_quantities': product_quantities,
    })


# from django.shortcuts import render
# from .models import Product

# # Analysis Page
# def analysis(request):
#     products = Product.objects.all()
    
#     # Categorizing products based on EOQ
#     high = [p for p in products if p.eoq >= 100]  # High EOQ
#     mid = [p for p in products if 50 <= p.eoq < 100]  # Mid EOQ
#     low = [p for p in products if p.eoq < 50]  # Low EOQ

#     data = {
#         'high': len(high),
#         'mid': len(mid),
#         'low': len(low),
#         'high_items': [{'name': p.item_name, 'eoq': p.eoq} for p in high],
#         'mid_items': [{'name': p.item_name, 'eoq': p.eoq} for p in mid],
#         'low_items': [{'name': p.item_name, 'eoq': p.eoq} for p in low],
#     }

#     return render(request, 'analysis.html', data)

from django.shortcuts import render
from .models import Product

# Analysis Page
def analysis(request):
    products = Product.objects.all()
    
    # Categorizing products based on price
    high = [p for p in products if p.price > 50000]  # High price
    mid = [p for p in products if 25000 <= p.price <= 50000]  # Mid price
    low = [p for p in products if p.price < 25000]  # Low price

    data = {
        'high': len(high),
        'mid': len(mid),
        'low': len(low),
        'high_items': [{'name': p.item_name, 'price': p.price} for p in high],
        'mid_items': [{'name': p.item_name, 'price': p.price} for p in mid],
        'low_items': [{'name': p.item_name, 'price': p.price} for p in low],
    }

    return render(request, 'analysis.html', data)

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re_password')

        if password != re_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')

        # Create a new user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.save()

        messages.success(request, "Registration successful! Please login.")
        return redirect('login')

    return render(request, 'register.html')

from django.contrib.auth import authenticate, login as auth_login  # Rename the imported login function
from django.shortcuts import render, redirect
from django.contrib import messages

def user_login(request):  # Rename the function
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)  # Use the renamed login function
            return redirect('display_page')  # Redirect to the home page after login
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'login.html')





def display_page(request):
    return render(request, 'display.html')

from django.contrib.auth import logout
from django.shortcuts import redirect

def user_logout(request):
    logout(request)  # Log out the user
    return redirect('login')  # Redirect to the login page after logout
