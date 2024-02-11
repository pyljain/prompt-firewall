import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial

_executor = ThreadPoolExecutor(10)

# Convert a sync operation to run asynchronously by executing in a thread pool
async def in_thread(func, *args, **kwargs):
    loop = asyncio.get_event_loop()
    partial_func = partial(func, *args, **kwargs)
    return await loop.run_in_executor(_executor, partial_func)