from fastapi import FastAPI
import uvicorn
import requests
import random
import json


app = FastAPI()

@app.get('/get_weighted_edges/')
def get_weighted_edges():
    topo_uri='http://127.0.0.1:5002/get_odl_topo/'
    edge_list = json.loads(requests.get(topo_uri).text)
    weighted_edge_list=[]
    for edge in edge_list:
        weighted_edge = {
            'v1':edge[0],
            'v2':edge[1],
            'w':round(random.random(),2)
        }
        weighted_edge_list.append(weighted_edge)
    return weighted_edge_list

if __name__ == '__main__':
    uvicorn.run(app=app,host='0.0.0.0',port=5003)
