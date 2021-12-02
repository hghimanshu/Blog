from typing import Any, Dict, Text, Union

import genos
from genos import get_class
import ray
import yaml
from fastapi import FastAPI
from ray import serve
from ray.serve.api import Deployment

from deployment import ModelDeployment


class Scaler:
    def __init__(self, model_dir: str, interpreter_class):
        self.model_dir = model_dir
        self.interpreter_class = interpreter_class
        self.model_name = "cifar"
        try:
            if not ray.is_initialized():
                ray.init(address="auto", namespace="serve")
        except Exception as e:
            raise Exception(f"Ray setup failed in either in ray cluster {e}")


    def get_depoyment_if_exists(self) -> Union[Deployment, None]:
        try:
            deployment = serve.get_deployment(name=self.model_name)
        except Exception:
            deployment = None
        return deployment

    
    def __check_if_replicas_are_correct(self, replicas: int):
        if replicas < 0:
            raise ValueError("Replica values must be positive !!")

    def model_loading(self, replicas: int) -> Dict[Text, Any]:
        self.__check_if_replicas_are_correct(replicas)
        deployment = self.get_depoyment_if_exists()
        response = {}
        
        if deployment is None:
            ## deployment doesn't exists !!
            ## scaleup then 
            print("deployment doesn't exists !!")
            ModelDeployment.options(
                num_replicas=replicas,
                route_prefix=f"/{self.model_name}",
                name=self.model_name
            ).deploy(self.model_dir, self.interpreter_class)
            response["message"] = "Successfully scaled up your model !!"
        else:
            ## deployment exists !!
            deployment.options(
                num_replicas=replicas
            ).deploy()
            response["message"] = "Successfully update replicas of your model !!"
        
        return response

    def model_parsing(self, input_path: str) -> Dict[Text, Any]:
        response = {}
        deployment = self.get_depoyment_if_exists()
        if deployment is None:
            response["message"] = "Sorry !! model haven't deployed yet. Please deploy your model before parsing."
        else:
            deployment_handle = deployment.get_handle()
            try:
                model_response = ray.get(deployment_handle.parse_message.remote(input_path))
            except Exception as e:
                model_response = "Something went wrong !!"
            response["message"] = model_response
        return response

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    with open('configs/scaler_config.yml') as f:
        config = yaml.safe_load(f)
        scaler = genos.recursive_instantiate(config=config)
    app.scaler = scaler


@app.post("/scaleup")
async def scaleup(
    replicas: int
):
    scale_response = app.scaler.model_loading(replicas)
    return scale_response

@app.post("/parse")
async def parse(
    input_image_path: str
):
    parsing_response = app.scaler.model_parsing(input_image_path)
    return parsing_response
