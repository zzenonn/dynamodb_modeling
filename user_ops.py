#!/usr/bin/env python3
import boto3
from boto3.dynamodb.conditions import Key

def create_user(username, fullname, email):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users-orders-items')
    
    user = {
        'pk'      : '#USER#{0}'.format(username), 
        'sk'      : 'PROFILE',
        'email'   : email,
        'address' : {}
    }
    table.put_item(Item=user)
    print("User {0} created".format(username))
    
def add_address(username, address_label, address):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users-orders-items')
    
    try:
        # Update item in table for the given username key.
        retsp = table.update_item(
            Key={'pk' : '#USER#{0}'.format(username),
                 'sk' : 'PROFILE'
            },
            UpdateExpression='SET address.#address = :address',
            ExpressionAttributeNames={'#address' : address_label},
            ExpressionAttributeValues={':address': address},
            ConditionExpression = "attribute_not_exists(address.#address)"
            )
        print("Address added")
    except Exception as err:
        print("Error message {0}".format(err))
        
def query_user_profile(username):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('users-orders-items')
    response = table.query(
        KeyConditionExpression=Key('pk').eq('#USER#{0}'.format(username)) & 
                               Key('sk').eq('PROFILE')
    )
    return response['Items']
