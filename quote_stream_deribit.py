import websockets
import asyncio
import json
from quote_stream import QuoteStream
from dataclasses import dataclass
from typing import List,Dict
from config import ws_base


@dataclass
class DeribitQuoteStream(QuoteStream):
    instrument_names: List[str]
    quotes: Dict[str,Dict[str,float]]
    

    def __post_init__(self):
        self.msg = \
            {"jsonrpc": "2.0",
             "method": "public/subscribe",
             "id": 42,
             "params": {
                 "channels": [f"quote.{instrument_name}"for instrument_name in self.instrument_names]}
            }
    def msg_init_qoute(self,symbol: str) -> Dict:
        msg = \
            {
            "jsonrpc" : "2.0",
            "id" : 8106,
            "method" : "public/ticker",
            "params" : {
                "instrument_name" : symbol
            }
            }
        return msg
    async def init_quotes(self,websocket):
        for i in range(len(self.instrument_names)):
            await websocket.send(json.dumps(self.msg_init_qoute(self.instrument_names[i])))
            response: str = await websocket.recv()
            temp = json.loads(response)
            symbol = temp['result']['instrument_name']
            self.quotes[symbol]['BidP'] = temp['result']["best_bid_price"]
            self.quotes[symbol]['AskP'] = temp['result']["best_ask_price"]
            self.quotes[symbol]['AskQ'] = temp['result']["best_ask_amount"]
            self.quotes[symbol]['BidQ'] = temp['result']["best_bid_amount"]





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
        
