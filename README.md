# Seldon practice

## Prerequisite

- Python
- Kubernetes
- Helm
- s2i

## Ambassador

Install

```bash
minikube addons enable ambassador
```

Test

```bash
kubectl get service ambassador -n ambassador
```

```bash
minikube tunnel
```

Notice that the ambassador service is exposed on external IP `127.0.0.1` with the help by `minikube tunnel`.

![](https://i.imgur.com/UapJNxO.png)

Now create a service

```bash
kubectl create deployment mapping-minikube --image=k8s.gcr.io/echoserver:1.4

kubectl expose deployment mapping-minikube --port=8080
```

```bash
kubectl get service mapping-minikube
```

```bash
kubectl port-forward service/mapping-minikube 8080:8080
```

![](https://i.imgur.com/50P4lT7.png)

Test the `mapping-minikube` service on Postman client.

Note that the service endpoing is `http://localhost:8080/`

![](https://i.imgur.com/42LEFdK.png)

We may apply the following CRD.
We map the mapping-minikube service to endpoint `/hello-mapping/`.

```yaml
apiVersion: getambassador.io/v2
kind:  Mapping
metadata:
  name:  mapping-minikube
spec:
  prefix: /hello-mapping/
  service: mapping-minikube.default:8080
```

![](https://i.imgur.com/vJRGW8j.png)

Test it on Postman client with the endpoint called `http://localhost/hello-mapping/`.

![](https://i.imgur.com/Keh2SqY.png)

Ref: [Using Ambassador Ingress Controller](https://minikube.sigs.k8s.io/docs/tutorials/ambassador_ingress_controller/)

## Seldon

### Install

Install the seldon by helm

```bash
kubectl create namespace seldon-system

helm install seldon-core seldon-core-operator --repo https://storage.googleapis.com/seldon-charts --set usageMetrics.enabled=true --namespace seldon-system --set ambassador.enabled=true
```

![](https://i.imgur.com/iBfOs0y.png)

Validate the installation
```
helm list -n seldon-system

kubectl get deployments -n seldon-system
```

![](https://i.imgur.com/LHbJHgs.png)

### Apply the SeldonDeployment

For simplicity, we test the trained model first.

```bash
kubectl create namespace seldon

kubectl apply -f sklearn.yml
```

```yaml
apiVersion: machinelearning.seldon.io/v1
kind: SeldonDeployment
metadata:
  name: iris-model
  namespace: seldon
spec:
  name: iris
  predictors:
  - graph:
      implementation: SKLEARN_SERVER
      modelUri: gs://seldon-models/sklearn/iris
      name: classifier
    name: default
    replicas: 1
  
```

Watch deployment status

```bash
kubectl get sdep -n seldon

kubectl get deployment -n seldon

kubectl rollout status <deployment-name> -n seldon
```

```bash
kubectl get pods -n seldon -w
```

![](https://i.imgur.com/kJhxu3X.png)

Test exposed service

Open browser, type `http://localhost/seldon/seldon/iris-model/api/v1.0/doc/`

![](https://i.imgur.com/MnGkofx.png)

Test prediction API

![](https://i.imgur.com/kjFEzmw.png)

Test on Postman client

![](https://i.imgur.com/23Kmqyl.png)

Ref: [Ingress with Ambassador](https://docs.seldon.io/projects/seldon-core/en/latest/ingress/ambassador.html)

### Apply the S2I image

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