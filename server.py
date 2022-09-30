import disnake
from disnake.ext import commands
from disnake import TextInputStyle
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import io
from io import BytesIO, StringIO
from PIL import Image, ImageOps
import asyncio
import queue
import time
import random
import requests
import json
import os
import shlex

ready = True
output = None

from dreams import dreams, input_queue

from commands import get_command_parser
from modals import PromptModal, ImageModal, InpaintingModal    

def parse(message):
    try:
        command_parser = get_command_parser()
        opts = command_parser.parse_known_args(shlex.split(message))
        return opts
    except Exception as e:
        print(e)
        return None

bot = commands.InteractionBot(test_guilds=[<your test server ID>])



scheduler = AsyncIOScheduler()
scheduler.add_job(dreams, 'interval', seconds=10)
scheduler.start()

@bot.event
async def on_reaction_add(reaction, user) -> None:
    print(reaction.emoji, user)
    print(reaction.message)

@bot.slash_command(description="Sanity test for prompts")
async def test_prompt(inter, message: str):
    options = parse(message)
    embed = disnake.Embed(title="Prompt Settings")
    for key, value in vars(options[0]).items():
        
        embed.add_field(
            name=key.capitalize(),
            value=value,
            inline=key != "prompt",
        )
    # print(inter.message)
    await inter.response.send_message(embed=embed)
    message = await inter.original_message()
    await message.add_reaction('🔄')
    await message.add_reaction('❌')
    # print(options)
    # await inter.response.send_message(json.dumps(vars(options[0])))

# @bot.slash_command(description="Run Prompt in Stable Diffusion") # this decorator makes a slash command
# async def generate(inter, message: str): # a slash command will be created with the name "ping"
#     options = parse(message)
    
#     await inter.response.defer()

#     input_queue.put_nowait({"text": f"Pong! Latency is {bot.latency}", "inter": inter, "opts": options})

@bot.slash_command(description="Power user prompt command")
async def generate(inter: disnake.AppCmdInter, message: str):
    options = parse(message)
    options = vars(options[0])
    
    if "prompt" in options and options["prompt"]:
        if isinstance(options["prompt"], list):
            options["prompt"] = " ".join(options["prompt"])
    
    await inter.response.send_message("queued!")
    
    input_queue.put_nowait({"text": f"Pong! Latency is {bot.latency}", "inter": inter, "opts": options})

@bot.slash_command(description="Run Prompt in Stable Diffusion")
async def inpainting(inter: disnake.AppCmdInter):
    """Sends a Modal to create a tag."""
    await inter.response.send_modal(modal=InpaintingModal())    

@bot.slash_command(description="Run Prompt in Stable Diffusion")
async def image2image(inter: disnake.AppCmdInter):
    """Sends a Modal to create a tag."""
    await inter.response.send_modal(modal=ImageModal())
    
@bot.slash_command(description="Run Prompt in Stable Diffusion")
async def prompts(inter: disnake.AppCmdInter):
    """Sends a Modal to create a tag."""
    await inter.response.send_modal(modal=PromptModal())