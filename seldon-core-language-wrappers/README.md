
# Seldon Core Language Wrappers

Activate the virtual environments

```bash
cd s2i/

python -m venv env

source env/bin/activate

python -m pip install -r requirements.txt
```

Train the model

```bash
python train.py
```

Create Python wrapper Model

```python
from joblib import load
class Model:
    def __init__(self):
        self._model = load("IrisClassifier.sav") 

    def predict(self, X, features_names=None):
        output = self._model.predict(X)
        return output
```

Test predict locally

```python
from Model import Model

model = Model()
model.predict([[5.964, 4.006, 2.081, 1.031]])
```

![](https://i.imgur.com/NmIBx2J.png)

```bash=
s2i -e PERSISTENCE=0 -e SERVICE_TYPE=MODEL -e MODEL_NAME=Model -e API_TYPE=REST build  . seldonio/seldon-core-s2i-python3:0.18 seldonio/sklearn-iris:0.1
```

Source to image
![](https://i.imgur.com/PrQ4Pbn.png)

Test on Postman client
![](https://i.imgur.com/1EIIDGB.png)

Push built image to registry

```bash
docker tag sklearn-iris:0.1 titaneric/sklearn-iris:0.1

docker push titaneric/sklearn-iris:0.1 
```

![](https://i.imgur.com/5dZxdLj.png)

Seldon Deploment CRD

```yaml=
apiVersion: machinelearning.seldon.io/v1alpha2
kind: SeldonDeployment
metadata:
  name: seldon-deployment-example
  namespace: seldon
spec:
  name: sklearn-iris-deployment
  predictors:
  - componentSpecs:
    - spec:
        containers:
        - image: titaneric/sklearn-iris:0.1
          imagePullPolicy: IfNotPresent
          name: sklearn-iris-classifier
    graph:
      children: []
      endpoint:
        type: REST
      name: sklearn-iris-classifier
      type: MODEL
    name: sklearn-iris-predictor
    replicas: 1
```

Expose ambassdor API
![](https://i.imgur.com/STriuof.png)

Test prediction on Seldon
![](https://i.imgur.com/rTmYtIZ.png)