import logging
import os
import shutil
import sys
from typing import Any, Dict, Optional, Text, Union
from fastapi import FastAPI, Header, HTTPException, Response
import psutil
import yaml


app = FastAPI()

@app.post("/deploy")
async def deploy(
    model_params: DeployParams,
    background_tasks: BackgroundTasks,
    response: Response = None,
    apikey: str = Header(None),
    superkey: Optional[str] = Header(None),
):
    return_if_recovery_mode()
    heimdall: NLUHeimdall = app.heimdall
    try:
        logger.info(f"MODEL PARAMS :: f{model_params}")
        if (
            override_heimdall()
            or superkey == get_superkey()
            and (superkey is not None and get_superkey() is not None)
        ):
            scheduler_results = await schedule_without_heimdall(
                apikey=apikey,
                model_params=model_params,
                response=response,
                superkey=superkey,
            )
        else:
            scheduler_results = await schedule_with_heimdall(
                heimdall=heimdall,
                apikey=apikey,
                model_params=model_params,
                response=response,
                superkey=superkey,
            )
        background_tasks.add_task(log_cluster_status)
        return scheduler_results
    except (ConnectionError, BrokenPipeError, ConnectionRefusedError):
        __kill_server()


@app.post("/async-deploy")
async def async_deploy(
    model_params: DeployParams,
    response: Response = None,
    apikey: str = Header(None),
    superkey: Optional[str] = Header(None),
):
    pass


@app.get("/health")
async def health():
    try:
        if recovery_health_file_path().exists():
            __set_recovery_mode()
        else:
            raise HTTPException(
                status_code=RECOVERY_MODE_CODE, detail=RECOVERY_MODE_MESSAGE
            )
        health_status = get_formatted_health_status(
            app.ray_scheduler.get_cluster_health()
        )
        return health_status
    except (ConnectionError, BrokenPipeError, ConnectionRefusedError):
        __kill_server()
