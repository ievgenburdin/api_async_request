import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor
# from tips.client import TipsClient


executor = ThreadPoolExecutor(max_workers=4)
loop = asyncio.get_event_loop()
# tips_client = TipsClient()
# loop.run_until_complete(tips_client.main())