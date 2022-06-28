

from queue import Queue
from typing import Dict, List

from trader_stream_deribit import MarketOrder


def strategy_main(quotes: Dict[str, Dict[str, float]],
                  positions: Dict[str, Dict[str, float]],
                  Trade_queue: Queue[MarketOrder],
                  sym: List[str]):
    perp_quote = quotes[sym[0]]
    fut_quote = quotes[sym[1]]

    pct_dif = 100*(fut_quote['BidP'] - perp_quote['AskP']) / perp_quote['AskP']
    print(pct_dif)
    if positions[sym[0]]['size'] == 0.0 and pct_dif > 0.00:
        Trade_queue.put_nowait(MarketOrder(True,sym[0],1))
        Trade_queue.put_nowait(MarketOrder(False,sym[1],1))
        print("Enter spread")
    elif abs(positions[sym[0]]['size']) > 0.0 and pct_dif < -0.01:
        Trade_queue.put_nowait(MarketOrder(False,sym[0],1))
        Trade_queue.put_nowait(MarketOrder(True,sym[1],1))
        print("exit spread")


    
