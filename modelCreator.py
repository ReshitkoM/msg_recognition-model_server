from models import *
from models.modelBase import ModelBase

class ModelCreator:

    def __init__(self):
        self.model = None
        self.availableModels = ModelBase.__subclasses__()

    def _find_model(self, lang) -> ModelBase:
        modelFound = False
        print(self.availableModels)
        for i in range(0, len(self.availableModels)):
            if self.availableModels[i].lang() == lang:
                self.model = self.availableModels[i]()
                modelFound = True

        if not modelFound:
            raise Exception("Cannot find suitable model!")

    def get_model(self, params) -> ModelBase:
        if self.model is None or self.model.lang() != params["lang"]:
            self._find_model(params["lang"])
            
        return self.model