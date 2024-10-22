import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
import yfinance as yf

class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join stock group
        self.stock_list = self.scope['url_route']['kwargs']['stock_list']
        self.group_name = f'stock_{self.stock_list}'

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        stock_symbol = text_data_json['symbol']

        # Fetch stock data
        stock_data = await self.get_stock_data(stock_symbol)

        # Send stock data to group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_stock_update',
                'message': stock_data
            }
        )

    async def send_stock_update(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

    @sync_to_async
    def get_stock_data(self, stock_symbol):
        stock = yf.Ticker(stock_symbol)
        hist = stock.history(period="1d")  # Adjust as needed
        price = hist['Close'].iloc[-1]  # Get the last close price
        return {
            'symbol': stock_symbol,
            'price': price,
            'timestamp': hist.index[-1].timestamp() * 1000,  # Convert to JS timestamp
        }
