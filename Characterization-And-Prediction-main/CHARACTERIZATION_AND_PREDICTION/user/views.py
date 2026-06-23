from django.shortcuts import render, redirect, get_object_or_404

from admins.models import Prodcuts
from user.forms import UsersForm, PurchaseForm
from user.models import Users, Purchase, Feedback
from user.words import positive_words, negative_words
from django.contrib import messages


def home(request):
    if 'admin' in request.session:
        del request.session['admin']

    products = Prodcuts.objects.all()
    return render(request, 'user/home.html', {'products': products})


def viewproduct(request, pk):
    pro = get_object_or_404(Prodcuts, id=pk)

    if request.method == "POST":
        
        if 'userid' not in request.session:
            messages.warning(request, "Please login first to add items to cart.")
            return redirect('user:index')

        uid = request.session['userid']
        uses = get_object_or_404(Users, id=uid)
        form = PurchaseForm(request.POST)

        if form.is_valid():
            ff = form.save(commit=False)
            ff.customer = uses
            ff.purhased = pro
            ff.totalprice = pro.price * ff.quantity
            ff.save()
            messages.success(request, "Item added to cart successfully!")
            return redirect('user:cart')
    else:
        form = PurchaseForm()

    return render(request, 'user/viewproduct.html', {'prod': pro, 'ipk': pk, 'form': form})


def cart(request):
    if 'userid' not in request.session:
        messages.info(request, "Please login to view your cart and checkout.")
        return redirect('user:index')

    uid = request.session['userid']
    uses = get_object_or_404(Users, id=uid)
    p = Purchase.objects.filter(customer=uses, status='incart')
    orders = Purchase.objects.filter(customer=uses, status='purchased').order_by('-created_at')

    if request.method == "POST":
        if 'userid' not in request.session:
            messages.error(request, "Session expired. Please login again.")
            return redirect('user:index')

        action = request.POST.get('action', '')
        delivery_address = request.POST.get('delivery_address', '')
        delivery_mobile = request.POST.get('delivery_mobile', '')

        if action == 'buynow':
            if not delivery_address or not delivery_mobile:
                messages.error(request, "Please enter delivery address and mobile number.")
                return render(request, 'user/cart.html', {'p': p, 'orders': orders})

            Purchase.objects.filter(customer=uses, status='incart').update(
                status='purchased',
                delivery_address=delivery_address,
                delivery_mobile=delivery_mobile
            )
            messages.success(request, "Payment successful! Your order has been placed.")
            p = Purchase.objects.filter(customer=uses, status='incart')
            orders = Purchase.objects.filter(customer=uses, status='purchased').order_by('-created_at')
            return render(request, 'user/cart.html', {'p': p, 'orders': orders})
        else:
            Purchase.objects.filter(customer=uses, status='incart').update(status='checkout')
            return redirect('user:home')

    return render(request, 'user/cart.html', {'p': p, 'orders': orders})


def viewratings(request, pk):
    pro = get_object_or_404(Prodcuts, pk=pk)
    fedbck = Feedback.objects.filter(product=pro)
    return render(request, 'user/viewratings.html', {'feedbacks': fedbck})


def addratings(request, pk):
    pos, neg = 0, 0
    sen = 'pending'
    pro = get_object_or_404(Prodcuts, pk=pk)
    uses = None
    stat = 'pending'

    try:
        uid = request.session['userid']
        uses = get_object_or_404(Users, id=uid)
    except:
        uses = None

    if uses:
        try:
            Purchase.objects.get(customer=uses, purhased=pro, status='purchased')
            stat = 'purchased'
        except:
            stat = 'not purchased'

    if request.method == "POST":
        if 'userid' not in request.session:
            messages.warning(request, "Please login first to add rating.")
            return redirect('user:index')

        ratings = request.POST.get('rating', '')
        comments = request.POST.get('comment', '')

        for pword in positive_words:
            if pword in comments:
                pos += 1

        for nword in negative_words:
            if nword in comments:
                neg += 1

        if pos > neg:
            sen = 'positive'
        elif neg > pos:
            sen = 'negative'
        else:
            sen = 'neutral'

        Feedback.objects.create(
            user=uses,
            product=pro,
            isPurchased=stat,
            rating=ratings,
            review=comments,
            sentiment=sen
        )
        messages.success(request, "Rating submitted successfully!")
        return redirect('user:home')

    return render(request, 'user/addratings.html', {'pro': pro})


def index(request):
    message = None
    if request.method == "POST":
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()

        users = Users.objects.filter(username=username, password=password).first()

        if users:
            request.session.flush()
            request.session['userid'] = users.id
            request.session['username'] = users.username
            return redirect('user:home')
        else:
            messages.error(request, "User name and password are not matching...")
            message = "User name and password are not matching..."

    return render(request, 'user/index.html', {'msg': message})

def registration(request):
    if request.method == "POST":
        loca = request.POST.get('location', '')
        users = UsersForm(request.POST)

        if users.is_valid():
            formss = users.save(commit=False)
            formss.location = loca
            formss.save()
            messages.success(request, "Registered successfully!")
            return redirect('user:index')
    else:
        users = UsersForm()

    return render(request, 'user/registration.html', {'form': users})


def order_detail(request, pk):
    if 'userid' not in request.session:
        messages.info(request, "Please login to view order details.")
        return redirect('user:index')

    uid = request.session['userid']
    uses = get_object_or_404(Users, id=uid)
    order = get_object_or_404(Purchase, id=pk, customer=uses)
    return render(request, 'user/order_detail.html', {'order': order})


def logout(request):
    request.session.flush()
    messages.success(request, "You have been logged out successfully!")
    return redirect('user:index')