from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb', 
                               region_name='us-west-2', 
                               aws_access_key_id='*********************', 
                               aws_secret_access_key='************************************')
    table = dynamodb.Table('pizza')

    menuId = event['menuId']
    store_name = event['store_name']
    selection = event['selection']
    size = event['size']
    price = event['price']
    store_hours = event['store_hours']

    response = table.put_item(
    Item={
        'menuId': menuId,
        'store_name': store_name,
        'selection':selection,
        'size' : size,
        'price' : price,
        'store_hours' : store_hours
    })
    print("PostItem succeeded now:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))
    return "200 OK"


