import io
import requests
from PIL import Image
import base64

def txt2img(prompt: str, 
            negative_prompt: str = "lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry", 
            steps: int = 28, 
            sampler_index: str = "Euler", 
            restore_faces: bool = False, 
            cfg_scale: float = 11, 
            height: int = 512, 
            width: int = 512,
            seed: int = -1,
            server_: str = "http://127.0.0.1:7860",
            *args):
    
    payload = {
        "prompt":prompt,
        "negative_prompt": negative_prompt,
        #There are tons of optional parms, let's just set the sampler
        "steps": min(steps, 50),
        "sampler_index": sampler_index,
        "cfg_scale": min(cfg_scale, 1),
        "width": min(width, 512),
        "height": min(height, 512),
        "seed": seed
    }
    
    resp = requests.post(url=f"{server_}/sdapi/v1/txt2img", json=payload)
    resp = resp.json()
    processed = Image.open(io.BytesIO(base64.b64decode(resp["images"][0])))
    return processed, resp["parameters"]