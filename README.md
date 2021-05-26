# Seldon practice

## Prerequisite

- Python
- Kubernetes
- Helm

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
