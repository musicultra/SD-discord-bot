import disnake
import queue
from auto_models import txt2img
import io
from io import BytesIO, StringIO
from PIL import Image, ImageOps
import requests
import json
import re

server_ = {
    "model_1": "http://127.0.0.1:7860",
    "model_2": "http://127.0.0.1:7860"
}
input_queue = queue.Queue(maxsize=100)
queue_limit = 100

"""
In the future we can show the results as they are forming here
"""
def send_image(inter, image, seed ):
    pass
    # print(inter, image, seed)
    # await inter.followup.send("image generated")
def step_image(inter, sample, step):
    pass

def create_image(options, inter):
    prompt = options["prompt"]
    negative = re.findall(r"\[(.*?)\]", prompt)
    negative = " ".join(negative).strip()
    positive = re.sub(r"\[(.*?)\]", "", prompt).strip()
                     
    options["prompt"] = positive
    options["negative_prompt"] = negative
    options["server_"] = server_[options["model"]]
    if "model" in options: del options["model"]

    return txt2img(**(options))

async def dreams():
    try:
        for i in range(queue_limit):
            prompt = input_queue.get_nowait()
            inter = prompt["inter"]
            
            if prompt["opts"] is None:
                await inter.followup.send("Error when parsing your request")
                continue
            
            options = prompt["opts"]
            embed = prompt["embed"]
            view = prompt["view"]

            image, parameters = create_image(options, inter)

            seed = parameters['seed']
            arr = io.BytesIO()
            image.save(arr, format='PNG')
            arr.seek(0)
            file = disnake.File(fp=arr, filename='test.png')
            
            embed.set_field_at(index=4, name="seed", value=seed)
            embed.set_image(file=file)
            
            await inter.followup.send(view=view, embed=embed, ephemeral=True)
    except queue.Empty:
        pass