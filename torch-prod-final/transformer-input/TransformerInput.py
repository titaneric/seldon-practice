import io
import json
import logging

import torchvision.transforms as transforms
from torch import FloatTensor
from PIL import Image

logger = logging.getLogger(__name__)
class TransformerInput:
    def __init__(self) -> None:
        self.imagenet_class_index = json.load(open("imagenet_class_index.json"))

    def transform_input(self, image, feats=None):
        my_transforms = transforms.Compose([transforms.Resize(255),
                                            transforms.CenterCrop(224),
                                            transforms.ToTensor(),
                                            transforms.Normalize(
                                                [0.485, 0.456, 0.406],
                                                [0.229, 0.224, 0.225])])
        image = Image.open(io.BytesIO(image))
        return my_transforms(image).unsqueeze(0).tolist()
