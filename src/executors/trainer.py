import json


import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from capsules.capsule.src.configs.config import CFG
from capsules.capsule.src.models.PackageModel import TrainExecutor,PackageModel,ConfigExecutor,TrainResponse,TrainOutputs,OutputData,PackageConfigs
from sdks.novavision.src.base.response import Response
from pydantic import ValidationError
from sdks.novavision.src.base.capsule import Capsule
from capsules.capsule.src.models.u_net_model import UNet

class Train(Capsule):
    def __init__(self, request, bootstrap):
        self.error_list = []
        try:
            super().__init__(request)

            self.request.model = PackageModel(**(self.request.data))
            self.batch_size = self.request.get_param("BatchSize")
            self.path = self.request.get_param("path")
        except ValidationError as e:
            self.error_list.append({"error": "error-unet-init"})

    @staticmethod
    def bootstrap():
        model = {"models": " "}
        return model

    def train(self):
       try:
            model = UNet(CFG,self.path,self.batch_size)
            model.load_data()
            model.build()
            model.train()
            model.evaluate()
            return True
       except:
            return False

    def run(self):
            #status=self.train()
            status=True
            outputImage = OutputData(value=[str(status)])
            trainOutputs = TrainOutputs(OutputData=outputImage)
            trainResponse = TrainResponse(outputs=trainOutputs)
            trainExecutor = TrainExecutor(value= trainResponse)
            configExecutor = ConfigExecutor(value= trainExecutor)
            packageConfigs = PackageConfigs(executor=configExecutor)
            packageModel = PackageModel(configs=packageConfigs)
            return Response(model=packageModel).response()

