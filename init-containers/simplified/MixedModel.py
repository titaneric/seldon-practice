import io
import json
import os
import re

import torch
import torch.nn as nn
from torch import load
import torchvision.transforms as transforms
from torchvision.models import DenseNet
from PIL import Image
import seldon_core

# https://github.com/pytorch/vision/blob/882e11db8138236ce375ea0dc8a53fd91f715a90/torchvision/models/densenet.py#L224-L239
def _load_state_dict(model: nn.Module, model_url: str) -> None:
    # '.'s are no longer allowed in module names, but previous _DenseLayer
    # has keys 'norm.1', 'relu.1', 'conv.1', 'norm.2', 'relu.2', 'conv.2'.
    # They are also in the checkpoints in model_urls. This pattern is used
    # to find such keys.
    pattern = re.compile(
        r"^(.*denselayer\d+\.(?:norm|relu|conv))\.((?:[12])\.(?:weight|bias|running_mean|running_var))$"
    )

    state_dict = load(model_url)
    for key in list(state_dict.keys()):
        res = pattern.match(key)
        if res:
            new_key = res.group(1) + res.group(2)
            state_dict[new_key] = state_dict[key]
            del state_dict[key]
    model.load_state_dict(state_dict)

MODEL_NAME = "torch_model.pth"

class MixedModel:
    def __init__(self, model_uri) -> None:
        # path = "model_blob/densenet121-a639ec97.pth"
        # Make sure to pass `pretrained` as `True` to use the pretrained weights:
        self.model = DenseNet()
        model_file = os.path.join(
            seldon_core.Storage.download(model_uri), MODEL_NAME
        )
        _load_state_dict(self.model, model_file)
        # Since we are using our model only for inference, switch to `eval` mode:
        self.model.eval()

        self.imagenet_class_index = json.load(open("imagenet_class_index.json"))

    def predict(self, image_bytes, feats=None):
        image_bytes = self.transform_input(image_bytes)
        outputs = self.model.forward(torch.FloatTensor(image_bytes))
        _, y_hat = outputs.max(1)
        predicted_idx = str(y_hat.item())
        return self.imagenet_class_index[predicted_idx]

    def transform_input(self, image, feats=None):
        my_transforms = transforms.Compose([transforms.Resize(255),
                                            transforms.CenterCrop(224),
                                            transforms.ToTensor(),
                                            transforms.Normalize(
                                                [0.485, 0.456, 0.406],
                                                [0.229, 0.224, 0.225])])
        image = Image.open(io.BytesIO(image))
        return my_transforms(image).unsqueeze(0)