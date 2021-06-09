import json
import logging

from torch import FloatTensor

logger = logging.getLogger(__name__)

class TransformerOutput:
    def __init__(self) -> None:
        self.imagenet_class_index = json.load(open("imagenet_class_index.json"))

    def transform_output(self, outputs, feats=None):
        logger.info("Start transform")
        outputs = FloatTensor(outputs)
        logger.info(f"outputs shape is {outputs.size()}") 
        _, y_hat = outputs.max(1)
        predicted_idx = str(y_hat.item())
        logger.info("Finish transform")
        return self.imagenet_class_index[predicted_idx]

