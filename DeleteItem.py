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
            aws_access_key_id='*********************',
            aws_secret_access_key='***************************************',
            region_name='us-west-2')

    table = dynamodb.Table('pizza')

    menuId = event['params']['path']['menuid']
    
    print("Attempting a conditional delete...")

    try:
        response = table.delete_item(
            Key={
                'menuId': menuId
            }
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            print(e.response['Error']['Message'])
        else:
            raise
    else:
        print("DeleteItem succeeded:")
        print(json.dumps(response, indent=4, cls=DecimalEncoder))
    return response
