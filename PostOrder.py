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
                               aws_access_key_id='******************', 
                               aws_secret_access_key='**********************************')
    table = dynamodb.Table('order_pizza')

    menuId = event['menuId']
    order_id = event['order_id']
    customer_name = event['customer_name']
    customer_email = event['customer_email']

    response = table.put_item(
    Item={
        'order_id':order_id,
        'menuId': menuId,
        'customer_name': customer_name,
        'customer_email':customer_email
    })

    table = dynamodb.Table('pizza')
    response = table.get_item(
        Key={
            'menuId': menuId,
        }
    )
    
    selection = response['Item']['selection']

    count=0
    select = ""
    while count < len(selection):
        select+=str(count+1)+". "
        select +=selection[count]+" "
        count+=1
    print("Post Order success 200 OK")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))

    order_response = "Hi "+customer_name+" please choose one of these selection: "+select
    return order_response


