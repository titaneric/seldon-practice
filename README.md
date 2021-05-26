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

```Validate the installation
helm list -n seldon-system

kubectl get deployments -n seldon-system
```
