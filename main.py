from email.quoprimime import quote
from threading import Thread

from aiohttp import TraceDnsCacheHitParams

from quote_stream_deribit import DeribitQuoteStream
from position_stream_deribit import DeribitPositionStream
from trader_stream_deribit import DeribitTradeStream, MarketOrder
from time import sleep
import calender_spread_strategy

from queue import Queue

instrument_names = ['ETH-PERPETUAL','ETH-1JUL22']
# quotes = Queue(maxsize = 1)

quotes = {
    'ETH-PERPETUAL': {'BidQ':0.0,'BidP':0.0,'AskQ':0.0,'AskQ':0.0,},
    'ETH-1JUL22': {'BidQ':0.0,'BidP':0.0,'AskQ':0.0,'AskQ':0.0,},
}

positions = {
    'ETH-PERPETUAL': {'size':0.0,'AvgP':0.0},
    'ETH-1JUL22': {'size':0.0,'AvgP':0.0},
}

Trade_queue: Queue[MarketOrder] = Queue()

deribit_quote_stream = DeribitQuoteStream(instrument_names,quotes)
quote_thread = Thread(target=deribit_quote_stream.start_stream)
quote_thread.daemon = True
quote_thread.start()

deribit_position_stream = DeribitPositionStream(instrument_names,positions)
position_stream = Thread(target=deribit_position_stream.start_stream)
position_stream.daemon = True
position_stream.start()

deribit_trade_stream = DeribitTradeStream(Trade_queue)
trade_stream = Thread(target=deribit_trade_stream.start_stream)
trade_stream.daemon = True
trade_stream.start()

sleep(2)

while True:
    sleep(1)
    calender_spread_strategy.strategy_main(quotes,positions,Trade_queue,instrument_names)
    # Trade_queue.put_nowait(MarketOrder(True,'ETH-PERPETUAL',1))

    # print(f"quotes : {quotes}")
    print(f"positions : {positions}")
    
