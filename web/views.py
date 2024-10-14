from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from .models import Product


def index(request):
    products = Product.objects.all()  # Fetch all products to display on the homepage
    return render(request, 'index.html', {'products': products})

def login(request):
    return render(request, 'login.html')

def list_view(request):
    user_products = Product.objects.filter(user=request.user)  # Get products of the logged-in user
    return render(request, 'list.html', {'user_products': user_products})

def signup(request):
    return render(request, 'signup.html')

def AP(request):
    return render(request, 'AP.html')

def CTUS(request):
    return render(request, 'CTUS.html')

def P1(request):
    return render(request, 'P1.html')
def P2(request):
    return render(request, 'P2.html')
def P3(request):
    return render(request, 'P3.html')
def P4(request):
    return render(request, 'P4.html')
def P5(request):
    return render(request, 'P5.html')

def addUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']

        if password == repassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username is already taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already in use')
                return redirect('signup')
            else:
                User.objects.create_user(
                    username=username,
                    first_name=firstname,
                    last_name=lastname,
                    email=email,
                    password=password
                )
                messages.success(request, 'User registered successfully')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
    return redirect('signup')

def loginForm(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('index')
        messages.error(request, 'Invalid username or password')
    return redirect('login')

def logout(request):
    auth.logout(request)
    return redirect('index')

def submit_product(request):
    if request.method == 'POST':
        product_name = request.POST.get("product_name")
        product_price = request.POST.get("product_price")

        # Create the product associated with the logged-in user
        Product.objects.create(
            user=request.user,
            name=product_name,
            price=product_price
        )
        return redirect('list')  # Redirect to the product list page
    return HttpResponse("Unauthorized", status=401)

def delete_product(request, product_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, id=product_id, user=request.user)
        product.delete()
        messages.success(request, 'Product deleted successfully')
        return redirect(request.META.get('HTTP_REFERER', 'index'))
    return HttpResponse("Unauthorized", status=401)

def list(request):
    return render(request, 'list.html')

class SubmitProductView(View):
    def post(self, request):
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')

        # Create a new Product instance
        Product.objects.create(name=product_name, price=product_price, user=request.user)

        # Redirect to the list page
        return redirect('list')
    
def delete_product_view(request, id):
    product = get_object_or_404(Product, id=id)
    product.delete()  # Deletes the product
    return redirect('list')  # Redirect back to the product list