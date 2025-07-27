import aiohttp


async def aioconect(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response = await response.json()
    if response.get('cod') == 200:
        return response
    else:
        raise ConnectionError
