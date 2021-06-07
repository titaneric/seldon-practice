import io
import os
import json

import torch
import torchvision.transforms as transforms
# from torchvision import models
from PIL import Image

import seldon_core

MODEL_NAME = "scripted_module.pth"

class MixedModel:
    def __init__(self, model_uri) -> None:
        # Make sure to pass `pretrained` as `True` to use the pretrained weights:
        # self.model = models.densenet121(pretrained=True)
        model_file = os.path.join(
            seldon_core.Storage.download(model_uri), MODEL_NAME
        )
        self.model = torch.jit.load(model_file)
        # Since we are using our model only for inference, switch to `eval` mode:
        self.model.eval()

        self.imagenet_class_index = json.load(open("imagenet_class_index.json"))

    def predict(self, image_list, feats=None):
        image_list = self.transform_input(image_list)
        outputs = self.model.forward(torch.FloatTensor(image_list))
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