#!/usr/bin/env python3
"""Create the UserOrders and OrderItems tables (Module 11 redesign)."""
import boto3

# Singapore. Change this if your tables live in another region.
REGION = 'ap-southeast-1'

USER_ORDERS_TABLE = 'UserOrders'
ORDER_ITEMS_TABLE = 'OrderItems'


def create_user_orders_table(dynamodb):
    # Users and their orders share one item collection, keyed by user_id.
    #   sk = 'PROFILE'         -> the user's profile
    #   sk = 'ORDER#<order_id>' -> one of the user's orders
    #
    # OrdersByStatus is a GSI with a multi-attribute sort key
    # (status, then created_at). Put the equality attribute first and the
    # range attribute last. Profiles have no status or created_at, so they
    # stay out of this index (sparse indexing).
    return dynamodb.create_table(
        TableName=USER_ORDERS_TABLE,
        AttributeDefinitions=[
            {'AttributeName': 'user_id',    'AttributeType': 'S'},
            {'AttributeName': 'sk',         'AttributeType': 'S'},
            {'AttributeName': 'status',     'AttributeType': 'S'},
            {'AttributeName': 'created_at', 'AttributeType': 'S'},
        ],
        KeySchema=[
            {'AttributeName': 'user_id', 'KeyType': 'HASH'},
            {'AttributeName': 'sk',      'KeyType': 'RANGE'},
        ],
        GlobalSecondaryIndexes=[{
            'IndexName': 'OrdersByStatus',
            'KeySchema': [
                {'AttributeName': 'user_id',    'KeyType': 'HASH'},
                {'AttributeName': 'status',     'KeyType': 'RANGE'},
                {'AttributeName': 'created_at', 'KeyType': 'RANGE'},
            ],
            'Projection': {'ProjectionType': 'ALL'},
        }],
        BillingMode='PAY_PER_REQUEST',
    )


def create_order_items_table(dynamodb):
    # Line items live in their own table. order_id is the partition key
    # (identifying relationship: an item always belongs to an order), so
    # "get all items for an order" is a base-table query.
    return dynamodb.create_table(
        TableName=ORDER_ITEMS_TABLE,
        AttributeDefinitions=[
            {'AttributeName': 'order_id', 'AttributeType': 'S'},
            {'AttributeName': 'item_id',  'AttributeType': 'S'},
        ],
        KeySchema=[
            {'AttributeName': 'order_id', 'KeyType': 'HASH'},
            {'AttributeName': 'item_id',  'KeyType': 'RANGE'},
        ],
        BillingMode='PAY_PER_REQUEST',
    )


if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb', region_name=REGION)

    for create in (create_user_orders_table, create_order_items_table):
        try:
            table = create(dynamodb)
            print("Creating {0}...".format(table.name))
            table.wait_until_exists()
            print("{0} is ready".format(table.name))
        except Exception as err:
            print("Table could not be created")
            print("Error message {0}".format(err))
