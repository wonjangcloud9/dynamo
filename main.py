import os
from dotenv import load_dotenv
import boto3

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()
load_dotenv(verbose=True)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
dynamodb = boto3.resource('dynamodb', region_name=os.environ.get("BOTO3_REGION"),
                          aws_access_key_id=os.environ.get("BOTO3_ID"),
                          aws_secret_access_key=os.environ.get("BOTO3_PW"))


@app.get("/")
async def root():
    return {"Table status:": "Hello"}


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id})


@app.get("/create")
async def create():
    movie_table = create_movie_table()
    return {"Table status:", movie_table.table_status}


def create_movie_table():
    table = dynamodb.create_table(
        TableName='Movies',
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


@app.get("/item")
def make_item():
    table = dynamodb.Table('DemoUsers')
    response = table.put_item(
        Item={
            'name': "wonjang3",
            'email': "test2@naver.com",
            'phone': "01022490110",
        }
    )
    return response


@app.get("/itemup")
def make_item():
    table = dynamodb.Table('DemoUsers')
    response = table.get_item(Key={'name': "wonjang3"})
    if response['Item'] is None:
        return {"no":"no"}
    return response["Item"]
