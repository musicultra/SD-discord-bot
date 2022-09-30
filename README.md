# Stable Diffusion Discord Bot
This discord bot server is made with rendering time in mind. It includes a queue for requests to be processed and handles async delivery of the results.


## This is a discord bot meant to work with InvokeAI and any fork of that repo

The repo should be placed in the same level as the ldm folder.

## To start the server, run
```python
from server import bot, scheduler
import asyncio

async def run():
    try:
        await bot.start("<bot id>")
    except KeyboardInterrupt:
        await bot.close()
await asyncio.create_task(run())
```
