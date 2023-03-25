from .modelBase import ModelBase
from .modelImplVosk import ModelImplVosk

class ModelRU(ModelBase):
    @staticmethod
    def lang():
        return "RU"

    def __init__(self) -> None:
        self.model = ModelImplVosk(model_name="vosk-model-small-ru-0.22")

    def predict(self, data):
        return self.model.predict(data)