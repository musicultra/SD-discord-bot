import disnake
from disnake.ext import commands
from disnake.enums import ButtonStyle
from disnake import TextInputStyle
import shlex
from commands import get_command_parser
from dreams import input_queue
import time
import os
from typing import Optional

def parse(message):
    try:
        command_parser = get_command_parser()
        opts = command_parser.parse_known_args(shlex.split(message))
        return opts
    except Exception as e:
        print(e)
        return None
    
def extract_from_embeds(embed):
    options = parse("")
    options = vars(options[0])
    
    for field in embed:
        key = field.name.lower()
        value = field.value
        
        if key in options:
            if value != 'None':
                if key == 'steps':
                    options[key] = int(value)
                elif key == 'width'or key == 'height':
                    options[key] = min(int(value), 1024)
                elif key == 'cfg_scale':
                    options[key] = max(float(value), 1.1)
                elif key == 'strength':
                    options[key] = min(float(value), 0.99)
                else:
                    options[key] = value
    options['seed'] = None
    return options
        
    
    
# Defines a simple view of row buttons.
class RowButtons(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(label="Re-roll", style=ButtonStyle.blurple)
    async def first_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):        
        await inter.response.send_message("Re-rolling.", ephemeral=True)
        
        options = extract_from_embeds(inter.message.embeds[0].fields)
        view = RowButtons()

        input_queue.put_nowait({"inter": inter, "opts": options, "embed": inter.message.embeds[0], "view": view})

    @disnake.ui.button(label="Delete", style=ButtonStyle.red)
    async def second_button(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.message.delete()
    
# Subclassing the modal.
class InpaintingModal(disnake.ui.Modal):
    def __init__(self):
        # The details of the modal, and its components
        components = [
            disnake.ui.TextInput(
                label="Image URL",
                placeholder="https://location-of-image.com",
                custom_id="init_img",
                style=TextInputStyle.short,
                max_length=200,
            ),
            disnake.ui.TextInput(
                label="Mask URL",
                placeholder="https://location-of-image.com",
                custom_id="init_mask",
                style=TextInputStyle.short,
                max_length=200,
            ),
            disnake.ui.TextInput(
                label="Strength (between 0 and 1)",
                placeholder="0.3",
                custom_id="strength",
                style=TextInputStyle.short,
                max_length=10,
                required=False
            ),
            disnake.ui.TextInput(
                label="CFG Guidence",
                placeholder="7.5",
                custom_id="cfg_scale",
                style=TextInputStyle.short,
                max_length=10,
                required=False
            ),
            disnake.ui.TextInput(
                label="Prompt",
                placeholder="Prompt goes here",
                custom_id="prompt",
                style=TextInputStyle.paragraph,
            ),
        ]
        
        super().__init__(
            title="Create Inpainting Prompt",
            custom_id="create_inpainting_prompt",
            components=components,
        )

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(title="Inpainting Creation")
        options = parse("")
        options = vars(options[0])
        options['strength'] = 0.3
        print(inter.text_values)
        for key, value in inter.text_values.items():
            if value == "":
                value = "Unknown" if key not in options else str(options[key])
            else:
                if key == "prompt":
                    options[key] = value
                elif key == "init_img":
                    if value == "https://location-of-image.com":
                        value = "None"
                    else:
                        options[key] = value
                elif key == "init_mask":
                    if value == "https://location-of-image.com":
                        value = "None"
                    else:
                        options[key] = value
                else:
                    try:
                        options[key] = float(value)
                        if key == "strength":

                                options[key] = min(float(value), 0.99)
                    except ValueError:
                        pass
                    
        for key, value in options.items():
            embed.add_field(
                name=key.capitalize(),
                value=value,
                inline=key != "prompt",
            ) 
        view = RowButtons()
        # print(options)
        await inter.response.send_message("queued!")
        # await inter.response.defer()
        
        input_queue.put_nowait({"inter": inter, "opts": options, "embed": embed, "view": view})

class ImageModal(disnake.ui.Modal):
    def __init__(self):
        # The details of the modal, and its components
        components = [
            disnake.ui.TextInput(
                label="Image URL",
                placeholder="https://location-of-image.com",
                custom_id="init_img",
                style=TextInputStyle.short,
                max_length=300,
            ),
            disnake.ui.TextInput(
                label="Strength (between 0 and 1)",
                placeholder="0.3",
                custom_id="strength",
                style=TextInputStyle.short,
                max_length=10,
                required=False
            ),
            disnake.ui.TextInput(
                label="CFG Guidence",
                placeholder="7.5",
                custom_id="cfg_scale",
                style=TextInputStyle.short,
                max_length=10,
                required=False
            ),
            disnake.ui.TextInput(
                label="Prompt",
                placeholder="Prompt goes here",
                custom_id="prompt",
                style=TextInputStyle.paragraph,
            ),
        ]
        super().__init__(
            title="Create Image Prompt",
            custom_id="create_image_prompt",
            components=components,
        )

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(title="Prompt Creation")
        options = parse("")
        options = vars(options[0])
        options['strength'] = 0.3
        print(inter.text_values)
        for key, value in inter.text_values.items():
            if value == "":
                value = "Unknown" if key not in options else str(options[key])
            else:
                if key == "prompt":
                    options[key] = value
                elif key == "init_img":
                    if value == "https://location-of-image.com":
                        value = "None"
                    else:
                        options[key] = value
                else:
                    try:
                        options[key] = float(value)
                        if key == "strength":

                                options[key] = min(float(value), 0.99)
                    except ValueError:
                        pass
                    
        for key, value in options.items():
            embed.add_field(
                name=key.capitalize(),
                value=value,
                inline=key != "prompt",
            ) 
        view = RowButtons()
        # print(options)
        await inter.response.send_message("queued!")
        # await inter.response.defer()
        
        input_queue.put_nowait({"inter": inter, "opts": options, "embed": embed, "view": view})

class PromptModal(disnake.ui.Modal):
    def __init__(self):
        # The details of the modal, and its components
        components = [
            disnake.ui.TextInput(
                label="Strength (between 0 and 1)",
                placeholder="0.75",
                custom_id="strength",
                style=TextInputStyle.short,
                max_length=10,
                required=False
            ),
            disnake.ui.TextInput(
                label="CFG Guidence",
                placeholder="7.5",
                custom_id="cfg_scale",
                style=TextInputStyle.short,
                max_length=10,
                required=False
            ),
            disnake.ui.TextInput(
                label="Width (multiple of 64) - Max 1024",
                placeholder="512",
                custom_id="width",
                style=TextInputStyle.short,
                max_length=10,
                required=False
            ),
            disnake.ui.TextInput(
                label="Height (multiple of 64) - Max 1024",
                placeholder="512",
                custom_id="height",
                style=TextInputStyle.short,
                max_length=10,
                required=False
            ),
            disnake.ui.TextInput(
                label="Prompt",
                placeholder="Prompt goes here.",
                custom_id="prompt",
                style=TextInputStyle.paragraph,
            ),
        ]
        
        super().__init__(
            title="Create Prompt",
            custom_id="create_prompt",
            components=components,
        )

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        # await inter.response.defer()
        # (Namespace(cfg_scale=7.5, height=512, init_img=None, init_mask=None, prompt=[], sampler_name='k_euler_a', steps=None, strength=0.75, upscale=None, width=512),
        embed = disnake.Embed(title="Prompt Creation")
        options = parse("")
        options = vars(options[0])
        # print(inter.text_values)
        for key, value in inter.text_values.items():
            if value == "":
                value = "Unknown" if key not in options else str(options[key])
            else:
                if key == "prompt":
                    options[key] = value
                elif key == "width" or key == "height":
                    try:
                        options[key] = min(int(value), 1024)
                    except ValueError:
                            pass
                else:
                    try:
                        options[key] = float(value)
                        if key == "strength":

                                options[key] = min(float(value), 0.99)
                    except ValueError:
                        pass


        for key, value in options.items():
            embed.add_field(
                name=key.capitalize(),
                value=value,
                inline=key != "prompt",
            ) 
        view = RowButtons()
        # print(options)
        await inter.response.send_message("queued!")
        # await inter.response.defer()
        
        input_queue.put_nowait({"inter": inter, "opts": options, "embed": embed, "view": view})
        
        # time.sleep(3)
        
        # await inter.followup.send("GONE")
        
        
