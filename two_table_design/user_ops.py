#!/usr/bin/env python3
"""User operations on the UserOrders table.

Access patterns served here:
  #1 Get user profile by username
  #2 Get all orders for a user
  #3 Get user profile + orders
  #5 Create a new user
"""
import boto3
from boto3.dynamodb.conditions import Key

from create_tables import REGION, USER_ORDERS_TABLE

dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(USER_ORDERS_TABLE)


def create_user(user_id, fullname, email):
    # Pattern #5. The profile is the 'PROFILE' item in the user's collection.
    user = {
        'user_id'  : user_id,
        'sk'       : 'PROFILE',
        'fullname' : fullname,
        'email'    : email,
        'address'  : {}
    }
    table.put_item(Item=user)
    print("User {0} created".format(user_id))


def add_address(user_id, address_label, address):
    try:
        table.update_item(
            Key={'user_id': user_id, 'sk': 'PROFILE'},
            UpdateExpression='SET address.#label = :address',
            ExpressionAttributeNames={'#label': address_label},
            ExpressionAttributeValues={':address': address},
            ConditionExpression='attribute_not_exists(address.#label)'
        )
        print("Address {0} added for {1}".format(address_label, user_id))
    except Exception as err:
        print("Error message {0}".format(err))


def get_user_profile(user_id):
    # Pattern #1. One GetItem on the base table, strongly consistent if needed.
    response = table.get_item(Key={'user_id': user_id, 'sk': 'PROFILE'})
    return response.get('Item')


def get_user_orders(user_id):
    # Pattern #2. Same partition, only the ORDER# sort keys.
    response = table.query(
        KeyConditionExpression=Key('user_id').eq(user_id) &
                               Key('sk').begins_with('ORDER#')
    )
    return response['Items']


def get_user_with_orders(user_id):
    # Pattern #3. One query returns the whole item collection:
    # the PROFILE item plus every ORDER# item. No GSI, no second call.
    response = table.query(
        KeyConditionExpression=Key('user_id').eq(user_id)
    )
    return response['Items']
