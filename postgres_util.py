from typing import Dict
import json
import requests


new_tree = {'position': '5-5','tag':'P1','tree_type':'Pommier','comments':'No comments','pictures':'http://test.com'}

def get_all_trees()->json:
    response = requests.get('http://127.0.0.1:8000/treeapi/trees/')
    return response.json()

def get_tree_from_tag(tag:str)->json:
    data={'tag':tag}
    response = requests.get('http://127.0.0.1:8000/treeapi/trees/', params=data)
    return response.json()

def update_tree(tag:str,new_values:Dict):
    id = get_tree_from_tag(tag)[0]['id']
    data_patch = new_values
    response = requests.patch(f'http://127.0.0.1:8000/treeapi/trees/{str(id)}/',data=data_patch)

def create_tree(values:Dict):
    response = requests.post('http://127.0.0.1:8000/treeapi/trees/', values)


#print(get_all_trees())
#print(get_tree_from_tag('P1'))
#update_tree('P1',{'tag':'P1','tree_type':'Fraise','comments':'youpi'})
#create_tree(new_tree)