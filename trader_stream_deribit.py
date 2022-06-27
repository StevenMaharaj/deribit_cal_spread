from queue import Queue
import websockets
import asyncio
import json
from dataclasses import dataclass
from typing import List,Dict
from config import ws_base


@dataclass
class DeribitTradeStream(QuoteStream):
    # instrument_names: List[str]
    Trade_queue: Queue
    

    def __post_init__(self):
        pass
        


    def limit(websocket):
        pass    

    def market(self,websocket,symbol:str,is_buy:bool,size:int):
        msg = \
        {
        "jsonrpc" : "2.0",
        "id" : 5275,
        "method" : "private/buy" if is_buy else "private/sell",
        "params" : {
            "instrument_name" : symbol,
            "amount" : size,
            "type" : "market",
            "label" : "market0000234"
        }
        }
        


    async def handle_messages(self):
        async with websockets.connect(f'{ws_base}/ws/api/v2') as websocket:
            await self.init_quotes(websocket)
            await websocket.send(json.dumps(self.msg))
            await websocket.recv()
            while websocket.open:
                response: str = await websocket.recv()
                temp = json.loads(response)
                symbol = temp['params']['data']['instrument_name']
                self.quotes[symbol]['BidQ'] = temp['params']['data']["best_bid_amount"]
                self.quotes[symbol]['BidP'] = temp['params']['data']["best_bid_price"]
                self.quotes[symbol]['AskP'] = temp['params']['data']["best_ask_price"]
                self.quotes[symbol]['AskQ'] = temp['params']['data']["best_ask_amount"]

    def start_stream(self):
        loop = asyncio.new_event_loop()
        task = loop.create_task(self.handle_messages())
        # loop.call_later(60, task.cancel)
        loop.run_until_complete(task)