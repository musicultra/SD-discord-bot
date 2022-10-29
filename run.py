from server import bot, scheduler
import asyncio

bot_token = "<token>"
async def run():
    try:
        await bot.start(bot_token)
    except KeyboardInterrupt:
        await bot.close()

loop = asyncio.get_event_loop()
task = loop.create_task(run())

loop.run_until_complete(asyncio.wait([task]))
loop.close()
