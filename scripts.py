import requests
from os.path import join, dirname, realpath

def call_app(endpoint, file=None, form_data=None):
    url = "http://127.0.0.1:5000" + endpoint
    print(f"call url: {url}")
    if file:
        files = {'file': open(file, 'rb')}
        resp = requests.post(url, files=files)
        return resp.url
    if form_data:
        resp = requests.post(url,data=form_data)
        print(resp.status_code)
        return resp.status_code




