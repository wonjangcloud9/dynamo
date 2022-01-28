from fastapi import FastAPI
from dotenv import load_dotenv
import boto3

app = FastAPI()
load_dotenv(verbose=True)


@app.get("/")
async def root():
    movie_table = create_movie_table()
    return {"Table status:", movie_table.table_status}


def create_movie_table():
    dynamodb = boto3.resource('dynamodb')
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
