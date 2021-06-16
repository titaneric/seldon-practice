import io
import json
import logging
import base64

import torchvision.transforms as transforms
from torchvision import models
from PIL import Image

logger = logging.getLogger(__name__)


class Transformer:
    def __init__(self) -> None:
        pass

    def transform_input_raw(self, request, feats=None):
        # logger.info(request)
        b64_file = request.get("binData", "")
        if b64_file:
            image = base64.b64decode(b64_file)
            my_transforms = transforms.Compose(
                [
                    transforms.Resize(255),
                    transforms.CenterCrop(224),
                    transforms.ToTensor(),
                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
                ]
            )
            image = Image.open(io.BytesIO(image))
            return {"data": {"ndarray": my_transforms(image).unsqueeze(0).tolist()}}

