import json
import tensorflow as tf
import numpy as np
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__),'../'))
from capsules.capsule.src.utils.config import Config
from capsules.capsule.src.configs.config import CFG
from sdks.novavision.src.media.image import Image
from capsules.capsule.src.models.PackageModel import SegmentationExecutor,PackageModel,PackageConfigs,SegmentationResponse,SegmentationOutputs,OutputData,ConfigExecutor
from sdks.novavision.src.base.response import Response
from sdks.novavision.src.base.capsule import Capsule
class Segmentation(Capsule):
    def __init__(self, request, bootstrap):
        self.error_list = []
        super().__init__(request)
        self.config = Config.from_json(CFG)
        self.image_size = self.config.data.image_size
        self.model =bootstrap["model"]
        self.predict = self.model.signatures["serving_default"]
        self.request.model = PackageModel(**(self.request.data))
        self.images = self.request.get_param("inputImage")
        self.is_list = Image.is_list(self.images)


    @staticmethod
    def bootstrap():
        config = Config.from_json(CFG)
        saved_path = config.project.path + '/capsules/capsule/src/weights/unet'
        model = tf.saved_model.load(saved_path)
        model = {"model":model}
        return model

    def preprocess(self, image):
        image = tf.image.resize(image, (self.image_size, self.image_size))
        return tf.cast(image, tf.float32) / 255.0

    def infer(self, image):
        tensor_image = tf.convert_to_tensor(image, dtype=tf.float32)
        tensor_image = self.preprocess(tensor_image)
        shape= tensor_image.shape
        tensor_image = tf.reshape(tensor_image,[1, shape[0],shape[1], shape[2]])
        print(tensor_image.shape)
        pred = self.predict(tensor_image)['conv2d_transpose_4']
        pred = pred.numpy().tolist()
        pred=json.dumps(pred)
        return json.loads(pred)

    def run(self):
        # pred_list = []
        #     for img in self.images:
        #         pred=self.infer(np.array(img.value))
        #         pred_list.append(pred)

            pred_list = []
            if (self.is_list):
                for img in self.images:
                    img = Image.get_image(img)
                    pred = self.infer(np.array(img.value))
                    pred_list.append(pred)
            else:
                img = Image.get_image(self.images)
                pred = self.infer(np.array(img.value))
                pred_list.append(pred)


            outputImage = OutputData(value=pred_list)
            segmentationOutputs = SegmentationOutputs(outputData=outputImage)
            segmentationResponse = SegmentationResponse(outputs=segmentationOutputs)
            segmentationExecutor = SegmentationExecutor(value=segmentationResponse)
            executor = ConfigExecutor(value=segmentationExecutor)
            packageConfigs = PackageConfigs(executor=executor)
            packageModel = PackageModel(configs=packageConfigs)
            return Response(model=packageModel).response()
