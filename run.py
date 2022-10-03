from server import bot, scheduler
import asyncio

bot = <token>
async def run():
    try:
        await bot.start(bot)
    except KeyboardInterrupt:
        await bot.close()
await asyncio.create_task(run())