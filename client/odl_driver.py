import requests
from requests.auth import HTTPBasicAuth
import json
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=2)

def get_odl_topo(controller_config:dict):
    host=controller_config['ip']
    port=controller_config['port']
    topo_endpoint=controller_config['endpoints']['topology']
    uname=controller_config['username']
    passwd=controller_config['password']
    odl_topo_endpoint = f'http://{host}:{port}/{topo_endpoint}'

    edge_list = []
    try:
        # fetch topo
        response = requests.get(odl_topo_endpoint, auth=HTTPBasicAuth(uname,passwd)).text
        topo_dict = json.loads(response)['network-topology']['topology']

        # build edgelist
        for link in topo_dict[0]['link']:
            source = link['source']['source-node']
            destination = link['destination']['dest-node']
            edge_list.append((source, destination))
    except:
        edge_list = None
    finally:
        return edge_list
