import odl_driver as odl
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import json
import os

app = FastAPI()

class InputData(BaseModel):
    data: dict

global edge_list
global path_list

@app.post('/set_odl_config/')
async def set_odl_config(payload:Request):
    odl_config = await payload.json()
    try:
        with open('odl_config.json','w') as fp:
            fp.write(json.dumps(odl_config, indent=2))
            return 'INFO: Configuration saved'
    except Exception as e:
        return {'Error': 'Config Failed', 'cause':str(e)}

@app.get('/get_odl_topo/')
def get_odl_topo():
    controller_config = None
    try:
        with open('odl_config.json','r') as fp:
            text = fp.read()
            controller_config = json.loads(text)
    except Exception as e:
        print(e)
    if controller_config:
        edge_list = odl.get_odl_topo(controller_config=controller_config)
        if edge_list == None:
            return('ERROR: Topology Fetch Error!')
        else:
            return JSONResponse(content=edge_list)
    else:
         return('ERROR: Error in Controller Config !')

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5002)