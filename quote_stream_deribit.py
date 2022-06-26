from symtable import Symbol
import websockets
import asyncio
import json
from queue import Queue
import requests
from quote_stream import QuoteStream
from dataclasses import dataclass
from typing import List,Dict

@dataclass
class DeribitQuoteStream(QuoteStream):
    instrument_names: List[str]
    quotes: Dict[str,List[float]]
    

    def __post_init__(self):
        self.msg = \
            {"jsonrpc": "2.0",
             "method": "public/subscribe",
             "id": 42,
             "params": {
                 "channels": [f"quote.{instrument_name}"for instrument_name in self.instrument_names]}
            }
        


    async def handle_messages(self):
        async with websockets.connect('wss://www.deribit.com/ws/api/v2') as websocket:
            await websocket.send(json.dumps(self.msg))
            await websocket.recv()
            while websocket.open:
                response: str = await websocket.recv()
                temp = json.loads(response)
                symbol = temp['params']['data']['instrument_name']
                self.quotes[symbol][0] = temp['params']['data']["best_bid_amount"]
                self.quotes[symbol][1] = temp['params']['data']["best_bid_price"]
                self.quotes[symbol][2] = temp['params']['data']["best_ask_price"]
                self.quotes[symbol][3] = temp['params']['data']["best_ask_amount"]

    def start_stream(self):
        loop = asyncio.new_event_loop()
        task = loop.create_task(self.handle_messages())
        # loop.call_later(60, task.cancel)
        loop.run_until_complete(task)
        
