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
            aws_access_key_id='***********************',
            aws_secret_access_key='***************************************',
            region_name='us-west-2')

    table = dynamodb.Table('order_pizza')

    order_id = event['params']['path']['order_id']
    
    try:
        response = table.get_item(
            Key={
                'order_id': order_id,
            }
        )
        return_response = {
                          "menuId":"","order_id":"","customer_name":"","customer_email":"",
                           "order_status":"",
                           "order":{
                                "selection":"","size":"","price":"","order_time":""      
                           }
                           }        
        return_response['menuId'] = response['Item']['menuId']
        return_response['order_id'] = response['Item']['order_id']
        return_response['customer_name']=response['Item']['customer_name']
        return_response['customer_email']=response['Item']['customer_email']
        return_response['order_status'] = response['Item']['order_status']
        return_response['order']['selection']=response['Item']['pizza_selection']
        return_response['order']['size']=response['Item']['pizza_size']
        return_response['order']['price']=response['Item']['pizza_price']
        return_response['order']['order_time']=response['Item']['order_time']

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response['Item']
        print("GetItem succeeded:")
        print(json.dumps(item, indent=4, cls=DecimalEncoder))
    return return_response
