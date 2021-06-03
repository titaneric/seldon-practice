from MixedModel import MixedModel

model = MixedModel("./")

# Test new transformed model
with open("../img/cat.jpg", "rb") as f:
    image = f.read()

# Test transformed model
print(model.predict(image))