from modelBase import ModelBase
from model import ModelImpl as Model

class ModelCreator:

    def __init__(self):
        self.model = None
        self.lang = None

    def get_model(self, params) -> ModelBase:
        if self.model is None or self.lang != params["lang"]:
            if params["lang"] == "EN":
                self.model = Model("vosk-model-small-en-us-0.15")

            if params["lang"] == "RU":
                self.model = Model("vosk-model-small-ru-0.22")
            
            self.lang = params["lang"]

        return self.model