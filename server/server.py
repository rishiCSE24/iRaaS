import graph_solver as gs 
import networkx as nx
from fastapi import FastAPI, Request 
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
import json
import os

app = FastAPI()

def compute_spf(graph:nx.Graph, algo:str, cutoff:int=None):
    # filter only switches 
    switches = [item for item in graph.nodes if item.split(':')[0]=='openflow']

    #all pair
    print('STATUS: Comnputing Paths')
    result = []
    for i in range(len(switches)):
        for j in range(i+1,len(switches)):
            routes = {}
            if not cutoff:
                cutoff = len(switches) 

            routes['v1'] = switches[i]
            routes['v2'] = switches[j]
            routes['paths'] = [ p 
                      for p 
                      in nx.all_shortest_paths(G=graph, 
                                               source=routes['v1'], 
                                               target=routes['v2'])
                      if len(p) < cutoff 
                    ]
            result.append(routes)
    return result

@app.get('/get_topo/')
async def download_image():
    # Return the file response when requested
    image_path='./topology.png'
    if os.path.exists(image_path):
        return FileResponse(image_path, media_type="image/png")
    else:
        return {"error": "Image not found"}

@app.post('/get_spf/')
async def get_spf(payload:Request):
    payload = await payload.json()
    mon_uri='http://127.0.0.1:5003/get_weighted_edges'
    if "cutoff" in payload:
        all_pair_routes = compute_spf(graph=gs.render_graph(mon_uri=mon_uri),
                                    algo=payload['algo'], 
                                    cutoff=payload['cutoff'])
    else:
        all_pair_routes = compute_spf(graph=gs.render_graph(mon_uri=mon_uri),
                                      algo=payload['algo'])
    response = {
        'routes': all_pair_routes,
        'topo_fig': '/get_topo'
        }
        
    return JSONResponse(response)

if __name__ == '__main__':
    uvicorn.run(app,host='0.0.0.0',port=5001)