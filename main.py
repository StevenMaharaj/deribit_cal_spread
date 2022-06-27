from email.quoprimime import quote
from threading import Thread

from quote_stream_deribit import DeribitQuoteStream
from position_stream_deribit import DeribitPositionStream
from time import sleep
import calender_spread_strategy

# from queue import Queue

instrument_names = ['ETH-PERPETUAL','ETH-1JUL22']
# quotes = Queue(maxsize = 1)

quotes = {
    'ETH-PERPETUAL': {'bidQ':0.0,'bidP':0.0,'AskQ':0.0,'AskQ':0.0,},
    'ETH-1JUL22': {'bidQ':0.0,'bidP':0.0,'AskQ':0.0,'AskQ':0.0,},
}

positions = {
    'ETH-PERPETUAL': {'size':0.0,'AvgP':0.0},
    'ETH-1JUL22': {'size':0.0,'AvgP':0.0},
}

deribit_quote_stream = DeribitQuoteStream(instrument_names,quotes)
quote_thread = Thread(target=deribit_quote_stream.start_stream)
quote_thread.daemon = True
quote_thread.start()

deribit_position_stream = DeribitPositionStream(instrument_names,positions)
position_stream = Thread(target=deribit_position_stream.start_stream)
position_stream.daemon = True
position_stream.start()

sleep(2)

while True:
    sleep(0.1)
    calender_spread_strategy.strategy_main(quotes,instrument_names)
    # print(f"quotes : {quotes}")
    # print(f"positions : {positions}")
    
