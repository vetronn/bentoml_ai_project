import numpy as np
import bentoml

# 1. Definujeme model ako 'Runner' (v novej verzii je to súčasť triedy)
iris_model = bentoml.sklearn.get("iris_clf:latest")

@bentoml.service(
    name="iris_classifier",
    traffic={
        "timeout": 60, 
        "api_max_latency_ms": 100,
        "api_max_batch_size": 10
    }
)
class IrisService:
    # Načítanie modelu priamo do servisu
    model_path = iris_model

    def __init__(self):
        # Toto nahradí starý 'runners' systém
        self.classifier = bentoml.sklearn.load_model(self.model_path)

    @bentoml.api(batchable=True, batch_dim=0) # <--- TU sa zapne batching
    def classify(self, input_series: np.ndarray) -> np.ndarray:
        return self.classifier.predict(input_series)