# Init-Containers

## Minio

Install Minio

```bash
kubectl create namespace minio-system

helm repo add minio https://helm.min.io/

helm install minio minio/minio --set accessKey=minioadmin --set secretKey=minioadmin --namespace minio-system
```

Open another terminal

```bash
kubectl rollout status deployment -n minio-system minio

kubectl port-forward -n minio-system svc/minio 8090:9000
```

Install `mc` CLI tool

```bash
GO111MODULE=on go get github.com/minio/mc
```

Add `mc` client (config alias)

```
mc config host add minio-seldon http://localhost:8090 minioadmin minioadmin

mc config host list
```
![](https://i.imgur.com/dLUeRv7.png)



Create bucket named `init-container` for config alias `minio-seldon`

```bash
mc mb minio-seldon/init-container -p

# validate it (-f flag shows the file)
mc tree minio-seldon -f
```

![](https://i.imgur.com/TlDG465.png)

Copy model into previously created bucket named `init-container`

```bash
mc cp densenet121-a639ec97.pth minio-seldon/init-container

# validate it
mc tree minio-seldon -f
```

![](https://i.imgur.com/C37K7KI.png)

Ref:
- [Install MinIO in cluster](https://docs.seldon.io/projects/seldon-core/en/latest/examples/minio_setup.html)
- [MinIO Client Complete Guide](https://docs.min.io/docs/minio-client-complete-guide.html)


## Rclone

Install rclone

```bash
go get github.com/rclone/rclone
```

Add config alias `minio-seldon` in rclone config

```bash
vim $(rclone config file)
```

![](https://i.imgur.com/Fg7KfnP.png)

Test rclone client

```bash
rclone lsd minio-seldon:

rclone ls minio-seldon:init-container
```

![](https://i.imgur.com/Y02Fnwi.png)

## Seldon Init Container

`SeldonDeployment` object use the default storage initializer defined in the following file.

![](https://i.imgur.com/mkmxgS7.png)

Steps

1. Create a volume
2. Mount volume into model and init container
3. Use `rclone` to download the model blob from modelUri to mounted volume in `init-container`
4. Model `classfier` load the model from mounted volume and predict.

For complete customized init container, see [init-container.yml](init-container.yml).

1. Create a secret called `mysecret`, define the rclone config and create a config alias `cluster-minio`.
2. Create a `SeldonDeployment` named `torch-server`.
1. Define two volumes, one for downloaded model path (`classifier-provision-location`), another for rclone config (`config`).
2. Define initContainers from image `rclone`
3. Mount the volume `classifier-provision-location` and `config` into `/mnt/models` and `/config/rclone` respectively.
4. Pass argument `copy cluster-minio:init-container /mnt/models` to download the model `*.pth` into `/mnt/models/*.pth`
5. Define container from image `torch-server
6. Mount the volume `classifier-provision-location` into `/mnt/models`
7. Define environment variable `PREDICTIVE_UNIT_PARAMETERS` and pass `model_uri` as an argument for model

Note that

1. Env `PREDICTIVE_UNIT_PARAMETERS` is defined in `seldon_core/microservice.py` 
> ![](https://i.imgur.com/1xQqT6n.png)
2. `rclone config file` show the default config path. In `rclone/rclone` image, default path is `/config/rclone/rclone.conf`.
> ![](https://i.imgur.com/B1aIm8z.png)

```bash
kubectl apply -f init-containers.yml
```

```bash
kubectl rollout status <deployment name>
```

```bash
kubectl logs <pod name> classifier
```

![](https://i.imgur.com/NnXOUu5.png)

![](https://i.imgur.com/JgU4kVa.png)

## Simplified Seldon Init Container

In [seldon-rclone-secret.yml](seldon-rclone-secret.yml), define the environment variable that could be read by`rclone`.

Environment variable define the config alias `mys3` for minio. 

```bash
kubectl apply -f seldon-rclone-secret.yml
```

Add new implementation `TORCH_SERVER` to `predictor_servers` key in `seldon-config` ConfigMap in namespace `seldon-system`.

```json
{
"TORCH_SERVER":{"protocols":{"seldon":{"defaultImageVersion":"0.3","image":"titaneric/torch-server"}}}
}
```

```bash
kubectl apply -f seldon-config.yml
```

Simplify the customizied init-container and server in [simplified-init-container.yml](simplified-init-container.yml).

Note that `seldon-rclone-secret` in envSecretRefName, `TORCH_SERVER` in implementation and `mys3:init-container` in modelUri.

```bash
kubectl apply -f simplified-init-container.yml
```

![](https://i.imgur.com/MRe6Ado.png)