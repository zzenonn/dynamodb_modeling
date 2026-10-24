#!/usr/bin/env python3
"""Order and line-item operations across UserOrders and OrderItems.

Access patterns served here:
  #4 Get all line items for an order
  #6 Place an order (create order + items)
  #7 Update order status
  #8 Update item status
  GSI: orders for a user by status, sorted/filtered by date
"""
import uuid
from datetime import datetime, timezone

import boto3
from boto3.dynamodb.conditions import Key

from create_tables import REGION, USER_ORDERS_TABLE, ORDER_ITEMS_TABLE

dynamodb = boto3.resource('dynamodb', region_name=REGION)
user_orders = dynamodb.Table(USER_ORDERS_TABLE)
order_items = dynamodb.Table(ORDER_ITEMS_TABLE)

# transact_write_items is a client call. The client that comes with the
# resource accepts plain Python values, just like table.put_item does.
client = dynamodb.meta.client


def checkout(user_id, address_label, cart, created_at=None):
    # Pattern #6. The order goes into UserOrders and its line items go into
    # OrderItems. A transaction writes both tables together: either the
    # order and all its items are saved, or nothing is.
    order_id = uuid.uuid4().hex[:6]
    created_at = created_at or datetime.now(timezone.utc).strftime('%Y-%m-%d')

    order = {
        'user_id'    : user_id,
        'sk'         : 'ORDER#{0}'.format(order_id),
        'order_id'   : order_id,
        'address'    : address_label,
        'status'     : 'Placed',
        'created_at' : created_at
    }
    writes = [{'Put': {'TableName': USER_ORDERS_TABLE, 'Item': order}}]

    for n, line in enumerate(cart, start=1):
        item = {
            'order_id'     : order_id,
            'item_id'      : 'itm{0:03d}'.format(n),
            'product_name' : line['product_name'],  # denormalized from Products
            'quantity'     : line['quantity'],
            'price'        : line['price'],
            'status'       : 'Pending'
        }
        writes.append({'Put': {'TableName': ORDER_ITEMS_TABLE, 'Item': item}})

    client.transact_write_items(TransactItems=writes)
    print("Order {0} placed for {1} with {2} items".format(order_id, user_id, len(cart)))
    return order_id


def get_order_items(order_id):
    # Pattern #4. Base-table query on OrderItems. No GSI needed.
    response = order_items.query(
        KeyConditionExpression=Key('order_id').eq(order_id)
    )
    return response['Items']


def update_order_status(user_id, order_id, status):
    # Pattern #7. Order status lives only on the order item in UserOrders.
    # The order must already exist.
    user_orders.update_item(
        Key={'user_id': user_id, 'sk': 'ORDER#{0}'.format(order_id)},
        UpdateExpression='SET #status = :status',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':status': status},
        ConditionExpression='attribute_exists(sk)'
    )
    print("Order {0} is now {1}".format(order_id, status))


def update_item_status(order_id, item_id, status):
    # Pattern #8. Items change independently of the order, which is one
    # reason they live in their own table.
    order_items.update_item(
        Key={'order_id': order_id, 'item_id': item_id},
        UpdateExpression='SET #status = :status',
        ExpressionAttributeNames={'#status': 'status'},
        ExpressionAttributeValues={':status': status},
        ConditionExpression='attribute_exists(item_id)'
    )
    print("Item {0} of order {1} is now {2}".format(item_id, order_id, status))


def get_orders_by_status(user_id, status, start_date=None, end_date=None):
    # OrdersByStatus GSI: equality on status, optional date range on
    # created_at. The range condition is always the last one.
    condition = Key('user_id').eq(user_id) & Key('status').eq(status)
    if start_date and end_date:
        condition = condition & Key('created_at').between(start_date, end_date)

    response = user_orders.query(
        IndexName='OrdersByStatus',
        KeyConditionExpression=condition
    )
    return response['Items']
