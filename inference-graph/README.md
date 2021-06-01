# Inference Graph

## PyTorch Example

We could fully leverage the feature of `pre-processor` or `post-processor`. We refer the [example](https://pytorch.org/tutorials/intermediate/flask_rest_api_tutorial.html) given on PyTorch.

```python
import io

import torchvision.transforms as transforms
from PIL import Image

def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)
```

function `transform_image` applies the series of transform and return PyTorch tensor.

```python
from torchvision import models
import json

imagenet_class_index = json.load(open('../_static/imagenet_class_index.json'))
# Make sure to pass `pretrained` as `True` to use the pretrained weights:
model = models.densenet121(pretrained=True)
# Since we are using our model only for inference, switch to `eval` mode:
model.eval()


def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return imagenet_class_index[predicted_idx]
```

PyTorch download the pretrained model and index json to predict and map the result.

## Test example locally

We could apply to model first

Install PyTorch library and prepare enviroments by pip.

Please install Python 3.7.0, you could install it by Anaconda.

```bash
cd inference-graph/

conda create --name py37 python=3.7

conda activate py37

python -m venv env

source env/bin/activate

mkdir whl && cd whl

python -m pip download torch==1.8.1+cpu torchvision==0.9.1+cpu torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html


python -m pip install -r requirements.txt -f ../whl/

wget https://s3.amazonaws.com/deep-learning-models/image-models/imagenet_class_index.json
```

```python
from MixedModel import MixedModel

model = MixedModel()

with open("img/cat.jpg", "rb") as f:
    print(model.predict(f))
```

![](https://i.imgur.com/N5aR9bV.png)


## Test S2I Python language wrapper

```
s2i -e PERSISTENCE=0 -e SERVICE_TYPE=MODEL -e MODEL_NAME=MixedModel -e API_TYPE=REST build -i ../whl/:/whl . seldonio/seldon-core-s2i-python3:1.9.0-dev mixed-model:0.1
```


```bash
docker run --rm -it -p 5000:9000 mixed-model:0.1
```

![](https://i.imgur.com/E15h5JK.png)

or 

```python
cd seldon/inference-graph
python client.py
```
## Decompose into two compoments

### Transformer

```python
cd transformer/

s2i -e PERSISTENCE=0 -e SERVICE_TYPE=TRANSFORMER -e MODEL_NAME=Transformer -e API_TYPE=REST build -i ../whl/:/whl . seldonio/seldon-core-s2i-python3:1.9.0-dev transformer:0.1

docker run --rm -it -p 5000:9000 transformer:0.1
```

![](https://i.imgur.com/nnDk9ZC.png)


### Model

```python
cd model/

s2i -e PERSISTENCE=0 -e SERVICE_TYPE=MODEL -e MODEL_NAME=Model -e API_TYPE=REST build -i ../whl/:/whl . seldonio/seldon-core-s2i-python3:1.9.0-dev model:0.1

docker run --rm -it -p 5000:9000 model:0.1
```

![](https://i.imgur.com/IVRLqre.png)

![](https://i.imgur.com/3tstA56.png)

Note that the error is quite normal, since we need to convert the input bytes into PyTorch tensor with the help of transformer.

Push to registry and apply seldon deployment

```bash
docker push titaneric/model:0.4

docker push titaneric/transformer:0.2

kubectl apply -f torch.yml

kubectl rollout status <deployment name>
```

```bash
minikube tunnel
```

![](https://i.imgur.com/k3cke2Z.png)


## Anaconda environment

```bash
cd conda

s2i -e PERSISTENCE=0 -e SERVICE_TYPE=MODEL -e MODEL_NAME=MixedModel -e API_TYPE=REST -e CONDA_ENV_NAME=py37 build . seldonio/seldon-core-s2i-python3:1.9.0-dev conda:0.1 
```