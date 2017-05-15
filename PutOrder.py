from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import datetime

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

    order_id = event['params']['path']['order_id']
    body = event['body-json']

    body_input = int(body['input'])
    
   
    table = dynamodb.Table('order_pizza')
    response_order = table.get_item(
        Key={
            'order_id': order_id
        }
    )
    menuId = response_order['Item']['menuId']

    table = dynamodb.Table('pizza')
    response_pizza = table.get_item(
        Key={
            'menuId': menuId
        }
    )
    print("I am here.......")
    
    size = ""
    selection = ""
    
    if response_order['Item'].has_key('pizza_selection'):
        size = response_pizza['Item']['size']
        size_selected = size[body_input-1]
        price = response_pizza['Item']['price']
        price_value = price[body_input-1]
        status = 'processing'
        time_of_order = str(datetime.datetime.now())
        order_response = "Your order costs will be"+str(price_value)+". We will email you when the order is ready. Thank you!"

        table = dynamodb.Table('order_pizza')
        response = table.update_item(
            Key={
                'order_id': order_id,
            },
            UpdateExpression="set  pizza_size= :s,pizza_price=:p,order_status=:os,order_time=:ot",
            ExpressionAttributeValues={
            ':s': size_selected,
            ':p': price_value,
            ':os': status,
            ':ot': time_of_order
            },
            ReturnValues="UPDATED_NEW"
        )
        print("Post Order success 200 OK")
        print(json.dumps(response, indent=4, cls=DecimalEncoder))

        return order_response

    else:
        selection = response_pizza['Item']['selection']
        pizza_selected = selection[body_input-1]
        size = response_pizza['Item']['size']
        count=0
        size_select = ""
        while count < len(size):
            size_select+=str(count+1)+". "
            size_select +=size[count]+" "
            count+=1
        table = dynamodb.Table('order_pizza')
        response = table.update_item(
            Key={
                'order_id': order_id,
            },
            UpdateExpression="set  pizza_selection= :s",
            ExpressionAttributeValues={
            ':s': pizza_selected
            },
            ReturnValues="UPDATED_NEW"
        )
        
        print("Post Order success 200 OK")
        print(json.dumps(response, indent=4, cls=DecimalEncoder))
        order_response = "Which size do you want? "+size_select
        return order_response

    
    


