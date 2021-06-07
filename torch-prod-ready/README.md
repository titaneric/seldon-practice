# Torch Production Ready

PyTorch enable [TorchScript](https://pytorch.org/docs/master/notes/serialization.html#recommended-approach-for-saving-a-model) module and it's recommended for saving a model.

> ..., serializes ScriptModules to a format that can be loaded in Python or C++. This is useful when saving and loading C++ modules or for running modules trained in Python with C++, a common practice when deploying PyTorch models.

Could be used in C++, may have a new C++ language wrapper for production!

Prepare transformed model

```bash
cd init-containers/complete

python transformed_model.py
```

Test transformed model

```bash
cd torch-prod-ready

python test_prod.py
```

![](https://i.imgur.com/X9lyOjI.png)

Prepare new prepackaged model server

```bash
s2i -e PERSISTENCE=0 -e SERVICE_TYPE=MODEL -e MODEL_NAME=MixedModel -e API_TYPE=REST build -e CONDA_ENV_NAME=py37 . seldonio/seldon-core-s2i-python3:1.9.0-dev torch-server:0.4
```

Test docker image locally

```bash
docker run -e PREDICTIVE_UNIT_PARAMETERS='[{"name":"model_uri","value":"/mnt/models","type":"STRING"}]' -v $(pwd):/mnt/models/ --rm -it -p 5000:9000 torch-server:0.4
```

```
docker tag torch-server:0.4 titaneric/torch-server:0.4

docker push titaneric/torch-server:0.4
```

Change version from 0.3 to 0.4

```
kubectl edit configmap seldon-config -n seldon-system
```

![](https://i.imgur.com/eLbVQjs.png)

```
kubectl apply -f simplified-init-container.yml
```

![](https://i.imgur.com/SJT9b3j.png)