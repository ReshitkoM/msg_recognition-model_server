from .modelImplVosk import ModelImplVosk
from .modelBase import ModelBase

class ModelEN(ModelBase):
    @staticmethod
    def lang():
        return "EN"
    
    def __init__(self) -> None:
        self.model = ModelImplVosk(modelName="vosk-model-small-en-us-0.15")

    def predict(self, data):
        return self.model.predict(data)
