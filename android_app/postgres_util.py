from typing import Dict
import json
import requests

#Exampleof tree to add
#new_tree = {'position': '5-5','tag':'P1','tree_type':'Pommier','comments':'No comments','pictures':'http://test.com'}

def login_and_get_token(username:str, password:str, url)->str:
    URL1=f'{url}accounts/login/'
    client = requests.session()
    # Retrieve the CSRF token first
    client.get(URL1)  # sets the cookie
    # login to app and get updated CSRF token
    login_data = dict(username=username, password=password, csrfmiddlewaretoken=client.cookies['csrftoken'])
    client.post(URL1, data=login_data)
    return client


with open("config.json",'r') as f:
    data = json.load(f)
    username = data[0]['auth']['username']
    password = data[0]['auth']['password']

env = 'dev'
if env == 'dev':
    url = 'http://127.0.0.1:8000/'
elif env == 'prod':
    url = 'http://farmcedric.herokuapp.com/'

client = login_and_get_token(username,password,url)
csrftoken = client.cookies['csrftoken']

def get_all_trees()->json:
    response = client.get(f'{url}treeapi/trees/', headers={"X-CSRFToken":csrftoken})
    return response.json()

def get_tree_from_tag(tag:str)->json:
    data={'tag':tag}
    response = client.get(f'{url}treeapi/trees/', params=data, headers={"X-CSRFToken":csrftoken})
    return response.json()

def update_tree(tag:str,new_values:Dict):
    id = get_tree_from_tag(tag)[0]['id']
    data_patch = new_values
    response = client.patch(f'{url}treeapi/trees/{str(id)}/', data=data_patch, headers={"X-CSRFToken":csrftoken})

def create_tree(values:Dict):
    response = client.post(f'{url}treeapi/trees/', values, headers={"X-CSRFToken":csrftoken})

def get_pic_from_index(id:int)->json:
    response = client.get(f'{url}treeapi/treepics/{str(id)}', headers={"X-CSRFToken":csrftoken})
    return response.json()

def create_treepic(values:Dict):
    file = open(values['treepic'],'rb')
    data = {'treetag':values['treetag']}
    files = {'treepic': file}
    response = client.post(f'{url}treeapi/treepics/', data=data, files=files,
                           headers={"X-CSRFToken":csrftoken})

def get_all_tree_pics()->json:
    response = client.get(f'{url}treeapi/treepics/', headers={"X-CSRFToken":csrftoken})
    return response.json()

def get_all_pics_from_a_tag(tag:str)->json:
    data ={'tag':tag}
    response = client.get(f'{url}treeapi/treepics/', params=data, headers={"X-CSRFToken":csrftoken})
    return response.json()



#create_treepic({'treetag':"X2",'treepic':"Capture.PNG"})
#print(get_all_tree_pics())
#print(get_all_pics_from_a_tag('X2'))

