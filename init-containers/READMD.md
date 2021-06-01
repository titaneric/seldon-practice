# Init-Containers

```bash
kubectl create namespace minio-system

helm repo add minio https://helm.min.io/

helm install minio minio/minio --set accessKey=minioadmin --set secretKey=minioadmin --namespace minio-system
```

![](https://i.imgur.com/JgU4kVa.png)