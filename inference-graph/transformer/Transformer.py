import io
import json

import torchvision.transforms as transforms
from torchvision import models
from PIL import Image

class Transformer:
    def __init__(self) -> None:
        pass

    def transform_input(self, image, feats=None):
        # file = request.files['binData']
        # image_bytes = file.read()
        my_transforms = transforms.Compose([transforms.Resize(255),
                                            transforms.CenterCrop(224),
                                            transforms.ToTensor(),
                                            transforms.Normalize(
                                                [0.485, 0.456, 0.406],
                                                [0.229, 0.224, 0.225])])
        image = Image.open(io.BytesIO(image))
        return my_transforms(image).unsqueeze(0).tolist()

