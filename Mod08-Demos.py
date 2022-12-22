# ============
# Create Table
# ============

import boto3

def create_movie_table(dynamodb=None):
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
            'ReadCapacityUnits': 400,
            'WriteCapacityUnits': 400
        }
    )
    return table

if __name__ == '__main__':
    movie_table = create_movie_table()
    print("Table status:", movie_table.table_status)


# ==========
# Load Table
# ==========
from decimal import Decimal
import json
import boto3

def load_movies(movies):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Movies')
    for movie in movies:
        year = int(movie['year'])
        title = movie['title']
        print("Adding movie:", year, title)
        table.put_item(Item=movie)

if __name__ == '__main__':
    with open("W:\My Documents\AWS\Demos\DevOnAWS\moviedata.json") as json_file:
        movie_list = json.load(json_file, parse_float=Decimal)
    load_movies(movie_list)

# ============
# Add item
# ============
import boto3

def put_movie(title, year, plot, rating):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('Movies')
    response = table.put_item(
       Item={
            'year': year,
            'title': title,
            'info': {
                'plot': plot,
                'rating': rating
            }
        }
    )
    return response

if __name__ == '__main__':
    movie_resp = put_movie("The Big New Movie", 2015,
                           "Nothing happens at all.", 0)
    print("Put movie succeeded:")
    print(movie_resp)

# ====================
# Query by year
# ====================
import boto3
from boto3.dynamodb.conditions import Key

def query_movies(year):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('Movies')
    response = table.query(
        KeyConditionExpression=Key('year').eq(year)
    )
    return response['Items']

if __name__ == '__main__':
    query_year = 1985
    print(f"Movies from {query_year}")
    movies = query_movies(query_year)
    for movie in movies:
        print(movie['year'], ":", movie['title'])

# ======================
# Scan the movies table
# ======================

from pprint import pprint
import boto3
from boto3.dynamodb.conditions import Key

def query_and_project_movies(year, title_range, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('Movies')
    print(f"Get year, title, genres, and lead actor")

    # Expression attribute names can only reference items in the projection expression.
    response = table.query(
        ProjectionExpression="#yr, title, info.genres, info.actors[0]",
        ExpressionAttributeNames={"#yr": "year"},
        KeyConditionExpression=
            Key('year').eq(year) & Key('title').between(title_range[0], title_range[1])
    )
    return response['Items']

if __name__ == '__main__':
    query_year = 1995
    query_range = ('A', 'L')
    print(f"Get movies from {query_year} with titles from "
          f"{query_range[0]} to {query_range[1]}")
    movies = query_and_project_movies(query_year, query_range)
    for movie in movies:
        print(f"\n{movie['year']} : {movie['title']}")
        pprint(movie['info'])

# ======================
# PartiQL Query for the Movies Table
# ======================

import boto3
import pandas as pd
import json

def query_movie(year):
    client = boto3.client('dynamodb')

    query = """SELECT year, title  
            FROM Movies
            WHERE year = {}""".format(year)

    print("The query is: " + query)

    response = client.execute_statement(Statement= query)
    return response

year = 1986
results = query_movie(year)
df = pd.json_normalize(results["Items"])
print(df)

# ==============
# Delete Table
# ==============
import boto3

def delete_movie_table():
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('Movies')
    table.delete()

if __name__ == '__main__':
    delete_movie_table()
    print("Movies table deleted.")

# ============
# Create Music Table
# ============

import boto3

def create_table(tablename,partitionkey):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.create_table(
        TableName=tablename,
        KeySchema=[
            {
                'AttributeName': partitionkey,
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': partitionkey,
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 400,
            'WriteCapacityUnits': 400
        }
    )
    return table

if __name__ == '__main__':
    new_table = create_table('MusicDemo','FullName')
    print("Table status:", new_table.table_status)


# ==========
# Load Table
# ==========
from decimal import Decimal
import pandas as pd
import json
import boto3

def load_data(tablename,items):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tablename)
    for tableitem in items:
        print("Adding item:", tableitem['FullName'])
        result = table.put_item(Item=tableitem)
        print(result)

if __name__ == '__main__':
    with open("W:\My Documents\AWS\Demos\DevOnAWS\MusicLibrary.json") as json_file:
        item_list = json.load(json_file, parse_float=Decimal)     
    load_data("MusicDemo",item_list)

# ======================
# PartiQL Query for the MusicLibrary
# ======================

import boto3
import pandas as pd

def query_music(artist):
    client = boto3.client('dynamodb')

    query = """SELECT Artist, Album, Title  
            FROM MusicDemo
            WHERE Artist = '{}'""".format(artist)

    print("The query is: " + query)

    response = client.execute_statement(Statement= query)
    return response

artist = "The Police"
results = query_music(artist)
df = pd.json_normalize(results["Items"])
print(df)

# ==============
# Delete Table
# ==============
import boto3

def delete_table(tablename):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table(tablename)
    table.delete()

if __name__ == '__main__':
    delete_table('MusicDemo')
    print("Table deleted.")


