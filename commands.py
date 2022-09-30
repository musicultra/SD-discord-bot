import argparse
import shlex

SAMPLER_CHOICES = [
    'ddim',
    'k_dpm_2_a',
    'k_dpm_2',
    'k_euler_a',
    'k_euler',
    'k_heun',
    'k_lms',
    'plms',
]

def get_command_parser(default_args={"width": 512, "height": 512, "sampler": "k_euler_a", "CFG": 7.5, "strength": 0.75}):
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-s', '--steps', type=int, help='Number of steps')
    parser.add_argument(
        '-W', '--width', type=int, help='Image width, multiple of 64', default=default_args["width"]
    )
    parser.add_argument(
        '-H', '--height', type=int, help='Image height, multiple of 64', default=default_args["height"]
    )
    parser.add_argument(
        '-A',
        '-m',
        '--sampler',
        dest='sampler_name',
        default=default_args["sampler"],
        type=str,
        choices=SAMPLER_CHOICES,
        metavar='SAMPLER_NAME',
        help=f'Switch to a different sampler. Supported samplers: {", ".join(SAMPLER_CHOICES)}',
    )
    parser.add_argument(
        '-C',
        '--cfg_scale',
        default=default_args["CFG"],
        type=float,
        help='Classifier free guidance (CFG) scale - higher numbers cause generator to "try" harder.',
    )
    parser.add_argument(
        '-f',
        '--strength',
        default=default_args["strength"],
        type=float,
        help='Strength for noising/unnoising. 0.0 preserves image exactly, 1.0 replaces it completely',
    )
    parser.add_argument(
        '-S',
        '--seed',
        type=int,
        default=None,
        help='Image seed; a +ve integer, or use -1 for the previous seed, -2 for the one before that, etc',
    )
    parser.add_argument(
        '-I',
        '--init_img',
        type=str,
        default=None,
        help='Path to input image for img2img mode (supersedes width and height)',
    )
    parser.add_argument(
        '-M',
        '--init_mask',
        type=str,
        default=None,
        help='Path to input mask for inpainting mode (supersedes width and height)',
    )
    parser.add_argument('prompt', nargs=argparse.REMAINDER)

    return parser
