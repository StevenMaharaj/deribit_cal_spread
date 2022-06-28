import json


def get_api_key(account_name: str, is_production: bool) -> tuple[str]:
    with open("deribit.json") as f:
        accounts: dict = json.load(f)
        if is_production:
            key = accounts['Production'][account_name]['client_id']
            secret = accounts['Production'][account_name]['client_secret']
        else:
            key = accounts['Test'][account_name]['client_id']
            secret = accounts['Test'][account_name]['client_secret']
    return (key, secret)


is_production = False
account_name = 'stevesm01'


client_id, client_secret = get_api_key(account_name, is_production)

if is_production:
    ws_base = "wss://www.deribit.com"
else:
    ws_base = "wss://test.deribit.com"
    
