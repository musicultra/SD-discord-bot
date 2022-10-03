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

from ldm.dream.restoration import Restoration

restoration = Restoration()

debug = False
esrgan = None
t2i = None
if not debug:
    esrgan = restoration.load_esrgan("experiments/pretrained_models/GFPGANv1.4.pth")

    t2i = Generate(
        model="waifu-diffusion-1.4",
        conf="./configs/models.yaml",
        sampler_name="k_euler_a",
        embedding_path=None,
        full_precision=False,
        precision="auto",
        gfpgan=None,
        codeformer=None,
        esrgan=esrgan
    )

    t2i.load_model()

    t2i.free_gpu_mem = False
    print("done")