from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, ExchangeOffer
from .forms import BookForm, ExchangeOfferForm, UserRegistrationForm, ExchangeRequestForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate


def book_list(request):
    books = Book.objects.all()
    return render(request, 'exchange/book_list.html', {'books': books})


@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'exchange/book_create.html', {'form': form})


def offer_create(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        form = ExchangeOfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.from_user = request.user
            offer.offered_book = book
            offer.save()
            return redirect('book_list')
    else:
        form = ExchangeOfferForm()
    return render(request, 'exchange/offer_create.html', {'form': form, 'book': book})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_list')
    else:
        form = UserCreationForm()
    return render(request, 'exchange/register.html', {'form': form})


@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user  # Призначити користувача, який створює книгу
            book.save()
            return redirect('book_list')  # Перенаправлення на список книг
    else:
        form = BookForm()

    return render(request, 'exchange/add_book.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user = authenticate(username=user.username, password=form.cleaned_data['password'])
            login(request, user)
            return redirect('book_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def create_exchange_request(request, offered_book_id):
    offered_book = get_object_or_404(Book, id=offered_book_id, owner=request.user)
    if request.method == 'POST':
        form = ExchangeRequestForm(request.POST)
        if form.is_valid():
            exchange_request = form.save(commit=False)
            exchange_request.offered_book = offered_book
            exchange_request.from_user = request.user
            exchange_request.to_user = exchange_request.requested_book.owner
            exchange_request.save()
            return redirect('book_list')
    else:
        form = ExchangeRequestForm()

    return render(request, 'exchange/create_exchange.html', {'form': form, 'book': offered_book})


@login_required
def my_exchanges(request):
    offers_sent = ExchangeOffer.objects.filter(from_user=request.user)
    offers_received = ExchangeOffer.objects.filter(to_user=request.user)

    return render(request, 'exchange/my_exchanges.html', {
        'offers_sent': offers_sent,
        'offers_received': offers_received,
    })


@login_required
def update_offer_status(request, offer_id, status):
    offer = get_object_or_404(ExchangeOffer, id=offer_id, to_user=request.user)

    if status not in ['accepted', 'rejected']:
        return redirect('my_exchanges')

    offer.status = status
    offer.save()

    return redirect('my_exchanges')
