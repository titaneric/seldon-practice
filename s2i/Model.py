from joblib import load
class Model:
    def __init__(self):
        self._model = load("IrisClassifier.sav") 

    def predict(self, X, features_names=None):
        output = self._model.predict(X)
        return output
    
    def health_ping(self):
        return "pong"