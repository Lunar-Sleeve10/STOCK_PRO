from django.urls import path
from .live_stock import LiveStockConsumer  # Update this import to match your file name

websocket_urlpatterns = [
    path('ws/stocks/', LiveStockConsumer.as_asgi()),  # Define the WebSocket URL path
]
