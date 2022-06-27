from tempfile import tempdir
from turtle import position
import websockets
import asyncio
import json
from queue import Queue
from quote_stream import QuoteStream
from dataclasses import dataclass
from typing import List, Dict
from config import client_id, client_secret, ws_base


@dataclass
class DeribitPositionStream(QuoteStream):
    instrument_names: List[str]
    positions: Dict[str, List[float]]

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
        self.msg_changes = \
            {"jsonrpc": "2.0",
             "method": "private/subscribe",
             "id": 42,
             "params": {
                 "channels": [f"user.changes.{symbol}.raw" for symbol in self.instrument_names]}
             }

        self.msg_posi_init = \
            {
                "jsonrpc": "2.0",
                "id": 2236,
                "method": "private/get_positions",
                "params": {
                    "currency": f"{self.instrument_names[0][:3]}",
                    "kind": "future"
                }
            }

    async def get_positions(self,websocket):
        await websocket.send(json.dumps(self.msg_posi_init))
        response: str = await websocket.recv()
        temp = json.loads(response)
        positions_list: List[Dict]= temp['result']
        for position in positions_list:
            symbol = position['instrument_name']
            side = -1.0 if position["direction"] == "sell" else 1.0
            self.positions[symbol]['size'] = side*position['size']
            self.positions[symbol]['AvgP'] = position['average_price']






    async def handle_messages(self):
        async with websockets.connect(f'{ws_base}/ws/api/v2') as websocket:
            await websocket.send(json.dumps(self.msgAuth))
            self.auth_info: Dict = await websocket.recv()
            await self.get_positions(websocket)
            await websocket.send(json.dumps(self.msg_changes))
            await websocket.recv()
            while websocket.open:
                response: str = await websocket.recv()
                temp = json.loads(response)

                positions_list = temp['params']['data']['positions']
                for position in positions_list:
                    symbol = position['instrument_name']
                    side = -1.0 if position["direction"] == "sell" else 1.0
                    self.positions[symbol]['size'] = side*position['size']
                    self.positions[symbol]['AvgP'] = position['average_price']
                    # self.positions[symbol][2] = position['total_profit_loss']

    def start_stream(self):
        loop = asyncio.new_event_loop()
        task = loop.create_task(self.handle_messages())
        # loop.call_later(60, task.cancel)
        loop.run_until_complete(task)
