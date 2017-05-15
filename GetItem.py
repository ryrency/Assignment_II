from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# Helper class to convert a DynamoDB item to JSON.
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
            aws_access_key_id='*************************',
            aws_secret_access_key='***************************************',
            region_name='us-west-2')

    table = dynamodb.Table('pizza')

    menuId = event['params']['path']['menuid']
    
    try:
        response = table.get_item(
            Key={
                'menuId': menuId,
            }
        )
        return_response = {
                          "menuId":"","store_name":"","selection":"","size":"",
                           "price":"", "store_hours" : ""
                           } 
        return_response['menuId'] = response['Item']['menuId']
        return_response['store_name'] = response['Item']['store_name']
        return_response['selection']=response['Item']['selection']
        return_response['size']=response['Item']['size']
        return_response['price'] = response['Item']['price']
        return_response['store_hours']=response['Item']['store_hours']
        
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Item']
        print("GetItem succeeded:")
        print(json.dumps(item, indent=4, cls=DecimalEncoder))
    return return_response
