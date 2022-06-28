from queue import Queue
import websockets
import asyncio
import json
from dataclasses import dataclass
from typing import List, Dict
from config import client_id, client_secret, ws_base


@dataclass
class MarketOrder:
    is_buy: bool
    symbol: str
    size: int


@dataclass
class DeribitTradeStream:
    # instrument_names: List[str]
    Trade_queue: Queue[MarketOrder]

    def __post_init__(self):
        self.msgAuth = \
            {
                "jsonrpc": "2.0",
                "id": 9929,
                "method": "public/auth",
                "params": {
                    "grant_type": "client_credentials",
                    "client_id": f"{client_id}",
                    "client_secret": f"{client_secret}"
                }
            }

    def limit(websocket):
        pass

    async def send_market_order(self, websocket, symbol: str, is_buy: bool, size: int):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 5275,
                "method": "private/buy" if is_buy else "private/sell",
                "params": {
                    "instrument_name": symbol,
                    "amount": size,
                    "type": "market",
                    "label": "market0000234"
                }
            }

        await websocket.send(json.dumps(msg))
        await websocket.recv()
        

    async def handle_messages(self):
        async with websockets.connect(f'{ws_base}/ws/api/v2') as websocket:
            await websocket.send(json.dumps(self.msgAuth))
            self.auth_info: Dict = await websocket.recv()
            while websocket.open:
                market_order = self.Trade_queue.get()
                await self.send_market_order(websocket,
                                       market_order.symbol,
                                       market_order.is_buy,
                                       market_order.size)

    def start_stream(self):
        loop = asyncio.new_event_loop()
        task = loop.create_task(self.handle_messages())
        # loop.call_later(60, task.cancel)
        loop.run_until_complete(task)
