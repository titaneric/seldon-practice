from MixedModel import MixedModel

model = MixedModel("./")

with open("../../img/cat.jpg", "rb") as f:
    image = f.read()

# Test original model
print(model.predict(image))

import torch

# Transform to TorchScript
scripted_module = torch.jit.script(model.model)

torch.jit.save(scripted_module, '../../torch-prod-final/scripted_module.pth')