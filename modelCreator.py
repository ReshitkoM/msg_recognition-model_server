import logging

from models import *
from models.modelBase import ModelBase

class ModelCreator:

    def __init__(self):
        self.model = None
        self.availableModels = ModelBase.__subclasses__()
        logging.info('Available models: %s.', self.availableModels)

    def _find_model(self, lang) -> ModelBase:
        modelFound = False
        for i in range(0, len(self.availableModels)):
            if self.availableModels[i].lang() == lang:
                self.model = self.availableModels[i]()
                modelFound = True
                break

        if not modelFound:
            raise Exception(f"Cannot find suitable model for language {lang}.")

    def get_model(self, params) -> ModelBase:
        if self.model is None or self.model.lang() != params["lang"]:
            self._find_model(params["lang"])
            
        return self.model