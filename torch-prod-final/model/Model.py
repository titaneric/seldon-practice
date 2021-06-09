import io
import json
import os

import torch
import seldon_core

MODEL_NAME = "scripted_module.pth"

class Model:
    def __init__(self, model_uri) -> None:
        model_file = os.path.join(
            seldon_core.Storage.download(model_uri), MODEL_NAME
        )
        self.model = torch.jit.load(model_file)
        # Since we are using our model only for inference, switch to `eval` mode:
        self.model.eval()


    def predict(self, image_bytes, feats=None):
        outputs = self.model.forward(torch.FloatTensor(image_bytes))
        # _, y_hat = outputs.max(1)
        # predicted_idx = str(y_hat.item())
        # return self.imagenet_class_index[predicted_idx]
        return outputs.tolist()
