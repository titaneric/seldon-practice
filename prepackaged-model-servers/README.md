# Prepackaged Model Servers

## Install seldon

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

## Apply the SeldonDeployment

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