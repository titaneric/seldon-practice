class IncrementModel:
    def __init__(self):
        pass

    def predict(self, X, features_names=None):
        output = X + 1
        return output
    
    def health_ping(self):
        return "pong"