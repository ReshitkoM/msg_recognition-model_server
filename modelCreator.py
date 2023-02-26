from modelBase import ModelBase
from model import ModelImpl as Model

class ModelCreator:

    def __init__(self):
        self.model = None

    def get_model(self, params) -> ModelBase:
        if self.model is None:
            self.model = Model()

        return self.model