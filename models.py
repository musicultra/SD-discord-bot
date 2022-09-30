import sys
sys.path.append('.')
from pytorch_lightning import logging
from omegaconf import OmegaConf
from ldm.generate import Generate

logging.getLogger('pytorch_lightning').setLevel(logging.ERROR)

# these two lines prevent a horrible warning message from appearing
# when the frozen CLIP tokenizer is imported
import transformers

transformers.logging.set_verbosity_error()

t2i = Generate(
    width=512, # num
    height=512, # num
    sampler_name='k_lms', #sampler
    weights='models/stable-diffusion-1.4.ckpt', # location of the weights
    full_precision=False, #use full precision
    config='configs/stable-diffusion/v1-inference.yaml', # location of the config file
    grid=False, # false
    steps=50,
    # this is solely for recreating the prompt
    seamless=False, # false
    embedding_path=None, # NONE - custom concepts
    device_type='cuda', # cuda
    ignore_ctrl_c=False # false
)

t2i.load_model()
print("done")