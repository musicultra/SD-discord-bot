import disnake
import queue
from models import t2i
import io
from io import BytesIO, StringIO
from PIL import Image, ImageOps
import requests
import json

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
    options['step_increment'] = 5
    # image, seed, first_seed=first_seed

    return t2i.prompt2image(
        image_callback=lambda image, seed, first_seed: send_image(inter, image, seed), 
        step_callback=None,
        **options)

async def dreams():
    try:
        # print("trying to enter the queue before another job finished")
        for i in range(queue_limit):
            prompt = input_queue.get_nowait()
            inter = prompt["inter"]
            
            if prompt["opts"] is None:
                await inter.followup.send("Error when parsing your request")
                continue
                
            options = prompt["opts"]
            
            
            if options["init_img"] != None:
                request = requests.get(options["init_img"])
                print(request.ok)
                if request.ok:
                    img_data = request.content
                    img = Image.open(BytesIO(img_data))
                    resize = ImageOps.contain(img, (512,512))
                    if resize.mode != "RGBA":
                        resize = resize.convert("RGBA")
                    resize.save("./temp_image.png", "png")
                    options["init_img"] = "./temp_image.png"
                else:
                    options["init_img"] = None
                    
            if options["init_mask"] != None:
                request = requests.get(options["init_mask"])
                print(request.ok)
                if request.ok:
                    img_data = request.content
                    img = Image.open(BytesIO(img_data))
                    resize = ImageOps.contain(img, (512,512))
                    if resize.mode != "RGBA":
                        resize = resize.convert("RGBA")
                    resize.save("./temp_mask_image.png", "png")
                    options["init_mask"] = "./temp_mask_image.png"
                else:
                    options["init_mask"] = None
            
            # options["prompt"] = " ".join(options["prompt"])
            result = create_image(options, inter)
            
            if len(result) == 0:
                await inter.followup.send("something went wrong")
                continue
            if len(result) != 0 and len(result[0]) == 0:
                await inter.followup.send("something went wrong")
                continue
                
            try:
                os.remove("./temp_image.png")
            except Exception as e:
                pass
            
            try:
                os.remove("./temp_mask_image.png")
            except Exception as e:
                pass
            
            image = result[0][0]
            arr = io.BytesIO()
            image.save(arr, format='PNG')
            arr.seek(0)
            file = disnake.File(fp=arr, filename='test.png')
            
            await inter.followup.send(file=file)
    except queue.Empty:
        pass