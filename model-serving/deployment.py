import os
from pathlib import Path
from typing import Union

from ray import serve

from cifar_interpreter import CIFARInterpreter


@serve.deployment
class ModelDeployment:
    def __init__(self, model_path: str, interpreter_class: type) -> None:
        self.model_interpreter: CIFARInterpreter = interpreter_class
        self.model_path = model_path
        self.loaded = False
        if self.model_interpreter.model is None:
            self.model_interpreter.create_interpreter(model_dir=Path(self.model_path))

    def __del__(self):
        pass

    async def parse_message(self, data: str) -> Union[None, str]:
        return await self.model_interpreter.model_parsing(data_path=data)
