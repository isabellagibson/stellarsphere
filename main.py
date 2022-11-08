import json
import fastapi
import requests
from urllib.parse import quote
import base64
from fastapi import Body, FastAPI, Header, Path, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from jinja2 import Template
from typing import Any, AnyStr, Optional, Union, List, Dict
from colorama import init, Fore
import json
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials

JSONBody = Union[List[Any], Dict[AnyStr, Any]]
init()
security = HTTPBasic()


def read_html(filename: str = None, data: dict = None):
    if not data:
        return '\n'.join(open(f'templates/{filename}.html', 'r').readlines())
    return Template('\n'.join(open(f'templates/{filename}.html', 'r').readlines())).render(data)


app = FastAPI(docs_url=None, redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'])
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

USERS = [
    {
        "username": "wgtech",
        "password": "whiteglove",
        "type": "whiteglove"
    },
    {
        "username": "eric",
        "password": "ihearttech",
        "type": "whiteglove"
    }
]


@app.get('/')
def index(request: fastapi.Request, credentials: HTTPBasicCredentials = Depends(security)):
    users = [
        user for user in USERS
        if user['username'] == credentials.username and
        user['password'] == credentials.password and
        user['type'] == 'whiteglove'
    ]
    if users == []:
        return templates.TemplateResponse(name='401.html', context={'request': request})
    return templates.TemplateResponse(name='index.html', context={'request': request})


@app.get('/images')
def get_images(request: fastapi.Request):
    lines = requests.get(
        'https://chromiumdash.appspot.com/cros/download_serving_builds_csv?deviceCategory=Chrome%20OS').text.split('\n')
    HEADERS = [col for col in lines[0].split(',') if col != '']
    ROWS = [row.split(',')[:len(HEADERS)] for row in lines[1:]]
    return templates.TemplateResponse(name='images.html', context={'request': request, 'headers': HEADERS, 'rows': ROWS})


@app.post('/encode')
def encode_script(body: JSONBody = None):
    if not body:
        return False
    body = jsonable_encoder(body)
    lines = []
    for line in open('duck/base.txt', 'r').readlines():
        if 'REM {{ INTERNET_SETUP }}' in line:
            if body['use_wifi']:
                line = ''.join(open('duck/wifi.txt', 'r').readlines())
            else:
                line = 'DELAY 10000'
        if 'STRING {{ ACCOUNT_USERNAME }}' in line:
            line = f'STRING {body["email"]}\n'
        if 'STRING {{ ACCOUNT_PASSWORD }}' in line:
            line = f'STRING {body["password"]}\n'
        if 'REM {{ GET_SYSTEM_INFO }}' in line:
            if body['dump_system']:
                line = ''.join(
                    open('duck/get_system_info.txt', 'r').readlines())
        lines.append(line)
    duckycode = ''.join(lines)
    data = {
        'duck_type': 'encoder',
        'languageSelect': 'gb',
        'ducky_text': duckycode
    }
    resp = requests.post('https://ducktoolkit.com/encode', data=data).json()
    print(resp['valid'], resp['message'])
    file = resp['b64inject']
    return {'duckycode': duckycode, 'file': f'data:application/octet;base64,{file}'}


@app.get('/hook.js')
def get_hook(request: fastapi.Request):
    return FileResponse('duck/about_system.js')


@app.get('/save')
def save_about(data):
    if not data:
        return False
    data = json.loads(base64.b64decode(data.encode()).decode())
    print(f'{Fore.LIGHTYELLOW_EX}{"="*80}{Fore.RESET}')
    print(
        f'Model Name: {Fore.LIGHTGREEN_EX}{data["system_info"]["model_name"]}{Fore.RESET}')
    print(
        f'Model SKU: {Fore.LIGHTGREEN_EX}{data["system_info"]["sku_number"]}{Fore.RESET}')
    print(
        f'Serial Number: {Fore.LIGHTGREEN_EX}{data["system_info"]["serial_number"]}{Fore.RESET}')
    print(
        f'Chrome Version: {Fore.LIGHTGREEN_EX}{data["chrome_version"]}{Fore.RESET}')
    print(
        f'Model Codename: {Fore.LIGHTGREEN_EX}{data["model_codename"]}{Fore.RESET}')
    print(f'MAC Addresses:')
    for key in data['network_devices'].keys():
        # .split("/")[-1]
        print(
            f'  {Fore.CYAN}{key}{Fore.RESET}: {Fore.LIGHTGREEN_EX}{data["network_devices"][key]["Address"].upper()}{Fore.RESET}')
    print(f'{Fore.LIGHTYELLOW_EX}{"="*80}{Fore.RESET}')
    return True
