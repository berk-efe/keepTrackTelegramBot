import os

import json
import requests

from typing import Union

DEFAULT_SHOPS = [61, 16, 35, 48]  # Steam, Epic Games, GOG, Microsoft Store

SHOPS = {
    "steam": 61,
    "epic games": 16,
    "gog": 35,
    "microsoft store": 48,
}

def get_deals(country:str="TR", sort:str="-trending", limit:int=6, shops:list[str]=DEFAULT_SHOPS, max_price:int=None, min_cut:int=None) -> Union[dict, None]:
    """Get deals, you can get deals **sorting** and **limiting**<br>There are several sorting **options** such as:<br>
    **trending:** get the most trending deals
    <br>
    **max_price:** get the cheapest deals
    <br>
    **min_cut:** get deals with the highest sale rate
    <br>
    ...
    <br>
    you can reverse sort them with minus(-)
    
    Args:
        country (str, optional): country code. Defaults to "TR".
        sort (str, optional): sorting option. Defaults to "-trending".
        limit (int, optional): limit. Defaults to 6.
        shops (list[str], optional): list of shop names to filter deals. Defaults to DEFAULT_SHOPS. <br> CHECK SHOPS DICT FOR AVAILABLE SHOPS.
        max_price (int, optional): filter by max_price. Defaults to None.
        min_cut (int, optional): filter by min_cut. Defaults to None.
    
    Returns:
        Union[dict, None]: Returns a dictionary with game data or None if an error occurs.
    
    """

    """
    id
    slug
    
    title
    assets['boxart']
    assets['banner300']
    
    deal['shop'] {id, name}
    
    deal['price'] {amount, currency}
    deal['regular'] {amount, currency}
    
    deal['cut']
    deal['url']
    """
    _shops=[]
    for i in shops:
        if i not in SHOPS:
            print(f"ERROR: Shop ID {i} is not valid. Available shops: {SHOPS.keys()}")
            pass
        elif SHOPS[i] not in _shops:
            _shops.append(SHOPS[i])
        else:
            print(f"ERROR: Shop ID {i} is already included in the list. Skipping duplicate.")
    
    shops = _shops if _shops else DEFAULT_SHOPS       
    
    shop_str = ','.join(map(str, shops))

    url = f"https://api.isthereanydeal.com/deals/v2?country={country}&limit={limit}&sort={sort}&shops={shop_str}&key={os.environ.get('ITAD_API_KEY')}"


    payload = {}
    headers = {
    'Cookie': 'PHPSESSID=sv6vbd83btan3s8ipoootf0b57'
    }

    response = json.loads(requests.request("GET", url, headers=headers, data=payload).text)

    data=[]
    
    # There is an important error with deal['url']
    # i got timed out
    
    # further tests shows that it works okay with steam and epicgames

    list_of_games = response['list']
    
    for game in list_of_games:
        if game:
                
            info={}
            
            try:                
                info['price'] = game['deal']['price'] # {amount, currency}            
                info['cut'] = game['deal']['cut']
                
                if info['price']['amount'] > max_price and max_price is not None:
                    continue
                if info['cut'] < min_cut and min_cut is not None:
                    continue
            
                
                info['title'] = game['title']
                
                info['shop'] = game['deal']['shop'] # {id, name}
                info['regular'] = game['deal']['regular'] # {amount, currency}
                info['url'] = game['deal']['url']
            
            except KeyError as e:
                print(f"KeyError: {e} in game {game}")
                continue


            try:
                info['banner'] = game['assets']['banner600']
            except KeyError:
                info['banner'] = None
                
            
            data.append(info)

    return data if data else None
