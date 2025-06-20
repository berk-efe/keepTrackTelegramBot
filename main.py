import os
import asyncio

import telegram

from helper import get_deals 

TOKEN = os.getenv("BOT_API_KEY")
CHAT_ID = os.getenv("CHAT_ID")



async def main():
    bot = telegram.Bot(TOKEN)

    async with bot:
        info = get_deals(limit=50, shops=['steam', 'epic games', 'gog'], max_price=500, min_cut=50)
        if not info:
            await bot.send_message(chat_id=CHAT_ID, text="No deals found.")
            return

        for deal in info:
            if not deal:
                continue
            else:
                title = deal['title']
                banner = deal['banner']
                
                
                price = deal['price']['amount']
                regular = deal['regular']['amount']
                
                currency = deal['price']['currency']
                
                message = f"{title}\n{price} {currency} | ~~{regular} {currency}~~\n{deal['cut']}%\n{deal['shop']['name']}\n{deal['url']}"
                
                if not banner:
                    await bot.send_message(chat_id=CHAT_ID, text=message+"\n\nNo banner available.")
                else:        
                    await bot.send_photo(chat_id=CHAT_ID, caption=message, photo=banner)
        
        os._exit(0)
        
        
if __name__ == '__main__':
    asyncio.run(main())