from pathlib import Path
from typing import Union
from keras.models import load_model
import cv2


CIFAR_CLASSES = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

MODEL_INPUT_SIZE = (32, 32)
class CIFARInterpreter:
    def __init__(self) -> None:
        self.model = None

    def create_interpreter(self, model_dir: Path) -> None:
        if Path.exists(model_dir):
            self.model = load_model(model_dir)

    async def model_parsing(self, data_path: Path) -> Union[None, str]:
        prediction = None
        image = cv2.imread(data_path)
        image = cv2.resize(image, MODEL_INPUT_SIZE, interpolation= cv2.INTER_LINEAR)

        image = image.reshape(1, image.shape[0], image.shape[1], image.shape[2])
        if self.model:
            model_prediction = self.model.predict(image)[0].tolist()    
            index = model_prediction.index(max(model_prediction))

            prediction = CIFAR_CLASSES[index]
        return prediction