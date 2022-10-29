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
from modals import PromptModal, ImageModal, InpaintingModal, RowButtons   

def parse(message):
    try:
        command_parser = get_command_parser()
        opts = command_parser.parse_known_args(shlex.split(message))
        return opts
    except Exception as e:
        print(e)
        return None

bot = commands.InteractionBot(test_guilds=[])



scheduler = AsyncIOScheduler(job_defaults={'max_instances': 3})
scheduler.add_job(dreams, 'interval', seconds=10)
scheduler.start()

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
    view = RowButtons()
    await inter.response.send_message(view=view, embed=embed, ephemeral=True)

@bot.slash_command(description="Power user prompt command")
async def generate(inter: disnake.AppCmdInter, message: str):
    options = parse(message)
    options = vars(options[0])
    
    if "prompt" in options and options["prompt"]:
        if isinstance(options["prompt"], list):
            options["prompt"] = " ".join(options["prompt"])
    
    embed = disnake.Embed(title="Prompt Settings")
    for key, value in options.items():
        embed.add_field(
            name=key.capitalize(),
            value=value,
            inline=key != "prompt",
        )
    view = RowButtons()
    await inter.response.send_message("queued!", ephemeral=True)
    # await inter.response.defer()

    input_queue.put_nowait({"inter": inter, "opts": options, "embed": embed, "view": view})
    
    # input_queue.put_nowait({"text": f"Pong! Latency is {bot.latency}", "inter": inter, "opts": options})

# @bot.slash_command(description="Run Prompt in Stable Diffusion")
# async def inpainting(inter: disnake.AppCmdInter):
#     """Sends a Modal to create a tag."""
#     await inter.response.send_modal(modal=InpaintingModal())    

# @bot.slash_command(description="Run Prompt in Stable Diffusion")
# async def image2image(inter: disnake.AppCmdInter):
#     """Sends a Modal to create a tag."""
#     await inter.response.send_modal(modal=ImageModal())
    
@bot.slash_command(description="Run Prompt in Stable Diffusion")
async def prompts(inter: disnake.AppCmdInter):
    """Sends a Modal to create a tag."""
    await inter.response.send_modal(modal=PromptModal())
