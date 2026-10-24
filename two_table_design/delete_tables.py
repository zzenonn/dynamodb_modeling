#!/usr/bin/env python3
"""Delete the UserOrders and OrderItems tables when you are done."""
import boto3

from create_tables import REGION, USER_ORDERS_TABLE, ORDER_ITEMS_TABLE

if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb', region_name=REGION)

    for name in (USER_ORDERS_TABLE, ORDER_ITEMS_TABLE):
        table = dynamodb.Table(name)
        table.delete()
        table.wait_until_not_exists()
        print("{0} deleted".format(name))
