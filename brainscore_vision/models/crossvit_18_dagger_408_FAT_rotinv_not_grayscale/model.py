# -*- coding: utf-8 -*-
import functools
import os
from pathlib import Path

import torch
from timm.models import create_model

from brainscore_vision.model_helpers import download_weights
from brainscore_vision.model_helpers.activations.pytorch import (
    PytorchWrapper,
    load_images,
    preprocess_images,
)
from brainscore_vision.model_helpers.check_submission import check_models

BIBTEX = ""
LAYERS = [
    "blocks.1.blocks.1.0.norm1",
    "blocks.1.blocks.1.4.norm2",
    "blocks.2.revert_projs.1.2",
]

INPUT_SIZE = 256
IDENTIFIER = "crossvit_18_dagger_408_FAT_rotinv"
WEIGHT_PATH = os.path.join(os.path.dirname(__file__), "crossvit_FAT_rotinv_epoch5.pt")
# Description of Layers:
# Behavior : 'blocks.2.revert_projs.1.2'
# IT       : 'blocks.1.blocks.1.4.norm2'
# V1       : 'blocks.1.blocks.1.0.norm1'
# V2       : 'blocks.1.blocks.1.0.mlp.act'
# V4       : 'blocks.1.blocks.1.0.mlp.act'


def load_preprocess_custom_model(image_filepaths, image_size, **kwargs):
    images = load_images(image_filepaths)
    images = preprocess_images(images, image_size=image_size, **kwargs)
    return images


def get_model():
    download_weights(
        bucket="brainscore-vision",
        folder_path="models/crossvit_18_dagger_408_FAT_rotinv_not_grayscale",
        filename_version_sha=[
            (
                "crossvit_FAT_rotinv_epoch5.pt",
                "t1i9M5DDQon629Ge6BJ63iYIqbpLPDhb",
                "99c1686680540a3ec678f7a3c8d7133c28ba0631",
            )
        ],
        save_directory=Path(__file__).parent,
    )
    print(os.path.join(os.path.dirname(__file__)))

    # Generate Model
    model = create_model("crossvit_18_dagger_408", pretrained=False)
    checkpoint = torch.load(WEIGHT_PATH, map_location=torch.device("cpu"))
    model.load_state_dict(checkpoint["state_dict"], strict=True)
    model.eval()

    ### Load Model and create necessary methods
    # init the model and the preprocessing:
    preprocessing = functools.partial(load_preprocess_custom_model, image_size=224)
    # get an activations model from the Pytorch Wrapper
    activations_model = PytorchWrapper(
        identifier=IDENTIFIER, model=model, preprocessing=preprocessing
    )

    wrapper = activations_model
    wrapper.image_size = 224
    return wrapper


if __name__ == "__main__":
    # Use this method to ensure the correctness of the BaseModel implementations.
    # It executes a mock run of brain-score benchmarks.
    check_models.check_base_models(__name__)