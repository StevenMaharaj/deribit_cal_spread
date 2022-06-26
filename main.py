from email.quoprimime import quote
from threading import Thread

from quote_stream_deribit import DeribitQuoteStream
from time import sleep
# from queue import Queue

instrument_names = ['BTC-PERPETUAL','BTC-1JUL22']
# quotes = Queue(maxsize = 1)
quotes = {
    'BTC-PERPETUAL': [0.0,0.0,0.0,0.0,0.0],
    'BTC-1JUL22': [0.0,0.0,0.0,0.0,0.0],
}


deribit_quote_stream = DeribitQuoteStream(instrument_names,quotes)

t1 = Thread(target=deribit_quote_stream.start_stream)
t1.daemon = True
t1.start()

while True:
    sleep(1)
    print(quotes)
