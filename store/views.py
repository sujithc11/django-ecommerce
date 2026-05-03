from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Product,Cart,Order
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings



# Home Page
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


@login_required
def vendor_dashboard(request):
    if request.user.role != 'vendor':
        return redirect('home')

    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')

        Product.objects.create(
            vendor=request.user,
            name=name,
            description=description,
            price=price,
            image=image
        )

        return redirect('vendor_dashboard')

    # 🔥 THIS LINE IS MISSING IN YOUR CODE
    products = Product.objects.filter(vendor=request.user)

    return render(request, 'vendor_dashboard.html', {
        'products': products
    })

@login_required
def delete_product(request, id):
    product = Product.objects.get(id=id)

    if product.vendor == request.user:
        product.delete()

    return redirect('vendor_dashboard')

# Login
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


# Logout
def logout_user(request):
    logout(request)
    return redirect('login')

from django.contrib import messages

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        from .models import CustomUser

        # 🔥 CHECK IF USER EXISTS
        if CustomUser.objects.filter(username=username).exists():
            return render(request, 'signup.html', {
                'error': 'Username already exists'
            })

        user = CustomUser.objects.create_user(
            username=username,
            password=password,
            role=role
        )

        from django.contrib.auth import login
        login(request, user)

        if role == 'vendor':
            return redirect('vendor_dashboard')
        else:
            return redirect('home')

    return render(request, 'signup.html')
 

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')

@login_required
def cart(request):
    items = Cart.objects.filter(user=request.user)
    return render(request, 'cart.html', {'items': items})

@login_required
def remove_from_cart(request, cart_id):
    item = Cart.objects.get(id=cart_id)
    item.delete()
    return redirect('cart')

@login_required
def update_product(request, id):
    product = Product.objects.get(id=id)

    if request.method == "POST":
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.description = request.POST.get('description')

        if request.FILES.get('image'):
            product.image = request.FILES.get('image')

        product.save()
        return redirect('vendor_dashboard')

    products = Product.objects.filter(vendor=request.user)

    return render(request, 'vendor_dashboard.html', {
        'edit_product': product,
        'products': products
    })





@login_required
def buy_now(request, id):
    product = Product.objects.get(id=id)

    if request.method == "POST":
        address = request.POST.get('address')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        # ✅ Basic validation
        if not email:
            messages.error(request, "Email is required")
            return redirect(request.path)

        # Save order
        Order.objects.create(
            user=request.user,
            product=product,
            address=address,
            email=email,
            phone=phone
        )

        print("EMAIL ENTERED:", email)

        # ✅ Safe email sending
        try:
            send_mail(
                subject='Order Confirmation',
                message=f'Your order for {product.name} will arrive within 5 days 🗓️',
                from_email = settings.EMAIL_HOST_USER or "sujith11200411@example.com",
                recipient_list=[email],
                fail_silently=True,   # 🔥 show error in logs
            )
            print("Email sent successfully")

        except Exception as e:
            print("EMAIL ERROR:", e)

        return redirect('home')

    return render(request, 'address.html', {'product': product})