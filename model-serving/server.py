from fastapi import FastAPI

class temperature:
    def __init__(self):
        pass

    def convert_to_C(self, temp) -> float:
        temp_in_C = temp - 32
        temp_in_C = temp_in_C / 1.8
        return round(temp_in_C, 2)

    def convert_to_F(self, temp) -> float:
        temp_in_F = (temp * 1.8) + 32
        return round(temp_in_F, 2)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    temp_obj = temperature()
    app.temperature = temp_obj


@app.post("/covert_to_c")
async def covert_to_c(
    temperature: int
):
    temp_in_c = app.temperature.convert_to_C(temperature)
    return {"detail": "temperature after conversion is :: {}".format(temp_in_c)}

@app.post("/covert_to_f")
async def covert_to_f(
    temperature: int
):
    temp_in_f = app.temperature.convert_to_F(temperature)
    return {"detail": "temperature after conversion is :: {}".format(temp_in_f)}
