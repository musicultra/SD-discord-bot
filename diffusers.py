# Low cost image generation - works on Free GPU!

import torch
from torch import autocast
from diffusers import StableDiffusionPipeline

model_id = "CompVis/stable-diffusion-v1-4"
device = "cuda"
pipe = StableDiffusionPipeline.from_pretrained(
    model_id, torch_dtype=torch.float16, revision="fp16", use_auth_token=True)
pipe = pipe.to(device)

def generate_prompt(options):
    # Namespace(cfg_scale=7.5, height=512, init_img=None, init_mask=None, prompt=[], sampler_name='k_euler_a', steps=None, strength=0.75, upscale=None, width=512
    
    with autocast("cuda"):
        image = pipe(options['prompt'], 
            guidance_scale=options['cfg_scale'],
            height=512, 
            width=512, 
            num_inference_steps = 50 if options['steps'] is None else options['steps'], 
            seed = 'random', 
            scheduler = 'LMSDiscreteScheduler')["sample"][0]

    return image