# Torch Production Final

In this section, we de-couple the dependencies between transformed input, model prediction, and transformed output.

## Transformer Input

Load the image bytes and apply series of transformation including resize, crop and normalization.

```bash
cd transformer-input

s2i -e PERSISTENCE=0 -e SERVICE_TYPE=TRANSFORMER -e MODEL_NAME=TransformerInput -e API_TYPE=REST -e CONDA_ENV_NAME=py37 build . seldonio/seldon-core-s2i-python3:1.8.0 titaneric/transformer-input:1.0

docker push titaneric/transformer-input:1.0
```

## Model

Load the model binary from path, forward the result and transform it to `list` type.

```bash
cd model

s2i -e PERSISTENCE=0 -e SERVICE_TYPE=MODEL -e MODEL_NAME=Model -e API_TYPE=REST -e CONDA_ENV_NAME=py37 build . seldonio/seldon-core-s2i-python3:1.8.0 titaneric/torch-server:1.0

docker push titaneric/torch-server:1.0
```

## Transformer Output

Convert input type into PyTorch tensor, retrieve the index of highest probability in the tensor, and lookup the corresponding name for the index.

```bash
cd transformer-output

s2i -e PERSISTENCE=0 -e SERVICE_TYPE=TRANSFORMER -e MODEL_NAME=TransformerOutput -e API_TYPE=REST -e CONDA_ENV_NAME=py37 build . seldonio/seldon-core-s2i-python3:1.8.0 titaneric/transformer-output:1.0

docker push titaneric/transformer-output:1.0
```

## Apply the CRD

Change version from 0.4 to 1.0

```bash
kubectl edit configmap seldon-config -n seldon-system
```

![](https://i.imgur.com/VKOwrxQ.png)

Note that in the [./torch-prod-final.yml](./torch-prod-final.yml), the graph is described as `TRANSFORMER` for transformer-input, `OUTPUT_TRANSFORMER` for transformer-output.

```yaml
    graph:
      name: transformer-input
      type: TRANSFORMER
      children:
      - name: classifier
        implementation: TORCH_SERVER
        modelUri: mys3:init-container
        envSecretRefName: seldon-rclone-secret
        type: MODEL
        children: 
          - name: transformer-output
            type: OUTPUT_TRANSFORMER
```

```bash
kubectl apply -f torch-prod-final.yml
```

![](https://i.imgur.com/0BwHuAV.png)
