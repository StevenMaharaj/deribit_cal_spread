


from typing import Dict, List


def strategy_main(quotes: Dict[str,List[float]],sym:List[str]):
    perp_quote = quotes[sym[0]]
    fut_quote = quotes[sym[1]]
    
    pct_dif = 100*(fut_quote['BidP'] - perp_quote['BidP']  ) / perp_quote['BidP'] 
    print(pct_dif)