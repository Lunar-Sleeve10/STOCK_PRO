import yfinance as yf
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .forms import SignupForm, LoginForm
from .models import SavedStock
import json

# Home Page - Displays saved stocks and allows saving new stocks
@login_required
def home(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            stock_symbol = data.get('stock_symbol', '').upper()  # Get stock symbol from JSON
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        if stock_symbol:
            # Check if the stock is already saved
            existing_entry = SavedStock.objects.filter(user=request.user, stock_symbol=stock_symbol).first()

            if not existing_entry:
                # Add stock to saved stocks
                new_stock = SavedStock(user=request.user, stock_symbol=stock_symbol)
                new_stock.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Stock already saved'}, status=400)
        else:
            return JsonResponse({'error': 'Stock symbol not provided'}, status=400)
    
    # Handle GET requests and render the saved stocks
    saved_stocks = SavedStock.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'home.html', {'saved_stocks': saved_stocks})

# Signup page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()  # Saves the user with the password they choose
            return redirect('login')  # Redirect to login after signup
    else:
        form = SignupForm()  # Display the empty signup form
    return render(request, 'signup.html', {'form': form})

# Login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')  # Redirect to home page after successful login
    else:
        form = LoginForm()  # Display the empty login form
    return render(request, 'login.html', {'form': form})

# Logout page
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login after logout

# Fetch stock data for the graph
def get_stock_data(request):
    stock_symbol = request.GET.get('symbol', 'AAPL')
    stock = yf.Ticker(stock_symbol)
    hist = stock.history(period="1mo")  # Fetch 1-month historical data

    # Prepare data points for the graph
    datapoints = []
    for i, row in hist.iterrows():
        datapoints.append({
            'x': int(i.timestamp() * 1000),  # Ensure x is an integer (milliseconds)
            'y': row['Close']  # y is the closing stock price
        })

    return JsonResponse(datapoints, safe=False)

# Stock detail page
def stock_detail(request):
    stock_symbol = request.GET.get('symbol', '').upper()  # Get stock symbol from query parameters
    if not stock_symbol:
        return JsonResponse({'error': 'No stock symbol provided'}, status=400)

    try:
        stock = yf.Ticker(stock_symbol)
        data = stock.info  # Retrieve the stock information

        # Prepare the response data with checks for the keys' existence
        stock_data = {
            'name': data.get('longName', stock_symbol),
            'symbol': data.get('symbol', stock_symbol),
            'current_price': data.get('currentPrice', 'N/A'),
            'previous_close': data.get('previousClose', 'N/A'),
            'volume': data.get('volume', 'N/A'),
            'market_cap': data.get('marketCap', 'N/A'),
            'pe_ratio': data.get('forwardPE', 'N/A'),  # Using forward P/E ratio
            'price_change': data.get('regularMarketChange', 'N/A'),
            'price_change_percent': data.get('regularMarketChangePercent', 'N/A'),
        }

        return JsonResponse(stock_data)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# View saved stocks
@login_required
def saved_stocks(request):
    saved_stocks = SavedStock.objects.filter(user=request.user)
    stock_details = []

    # Fetch stock details for each saved stock
    for stock in saved_stocks:
        stock_info = get_stock_details(stock.stock_symbol)
        if stock_info:
            stock_info['id'] = stock.id  # Add the stock's database ID to the stock info
            stock_details.append(stock_info)

    return render(request, 'saved_stocks.html', {'stock_details': stock_details})

# Helper function to get stock details
def get_stock_details(stock_symbol):
    try:
        stock = yf.Ticker(stock_symbol)
        data = stock.info
        return {
            'name': data.get('longName', stock_symbol),
            'symbol': data.get('symbol', stock_symbol),
            'current_price': data.get('currentPrice', 'N/A'),
            'market_cap': data.get('marketCap', 'N/A'),
            'price_change': data.get('regularMarketChange', 'N/A'),
            'price_change_percent': data.get('regularMarketChangePercent', 'N/A'),
        }
    except Exception as e:
        return None

# Delete saved stock
@csrf_exempt
def delete_stock(request, stock_id):
    if request.method == 'DELETE':
        try:
            stock = get_object_or_404(SavedStock, id=stock_id, user=request.user)
            stock.delete()
            return JsonResponse({'success': True})
        except SavedStock.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Stock not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

# Fetch Nifty 50 data
def get_nifty_data(request):
    nifty = yf.Ticker("^NSEI")  # Nifty 50 index
    hist = nifty.history(period="1mo")  # Fetch 1 month of historical data

    # Prepare data points for the graph
    datapoints = []
    for i, row in hist.iterrows():
        datapoints.append({
            'x': int(i.timestamp() * 1000),  # Ensure x is an integer (milliseconds)
            'y': row['Close']  # y is the closing price
        })

    return JsonResponse(datapoints, safe=False)

# Fetch Sensex data
def get_sensex_data(request):
    sensex = yf.Ticker("^BSESN")  # Sensex index
    hist = sensex.history(period="1mo")  # Fetch 1 month of historical data

    # Prepare data points for the graph
    datapoints = []
    for i, row in hist.iterrows():
        datapoints.append({
            'x': int(i.timestamp() * 1000),  # Ensure x is an integer (milliseconds)
            'y': row['Close']  # y is the closing price
        })

    return JsonResponse(datapoints, safe=False)

# Logout page
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login after logout
