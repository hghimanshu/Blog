import os
from pathlib import Path
from typing import Any, Dict, List, Text, Union

from ray import serve
from ray.util.queue import Queue
from starlette.requests import Request
from starlette.responses import JSONResponse
from cifar_interpreter import CIFARInterpreter

@serve.deployment
class ModelDeployment:
    def __init__(self, model_path: str, interpreter_class: type) -> None:
        self.model_interpreter: CIFARInterpreter = interpreter_class()
        self.model_path = model_path
        self.loaded = False
        if self.model_interpreter.model is None:
            self.model_interpreter.create_interpreter(model_dir=Path(self.model_path))

    def __del__(self):
        pass

    async def parse_message(self, data: str) -> Dict[Text, Any]:
        return await self.model_interpreter.model_parsing(data_path=Path(data))

    async def __parse(self, request: Request) -> Dict[Text, Any]:
        input_text = request.query_params["text"]
        data = {"text": input_text}
        result = await self.model_interpreter.parse(data=data)
        final_result = {OUTPUT: result}
        return final_result