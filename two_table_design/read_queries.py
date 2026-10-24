#!/usr/bin/env python3
"""Run each access pattern against the two-table design."""
import user_ops as user
import order_ops as order


def show_order(o):
    print("  {0}  {1:<10} {2}  ship to: {3}".format(
        o['order_id'], o['status'], o['created_at'], o['address']))


def show_items(order_id):
    for i in order.get_order_items(order_id):
        print("    {0}  {1:<48} x{2:<3} {3:>8}  {4}".format(
            i['item_id'], i['product_name'], i['quantity'], i['price'], i['status']))


if __name__ == '__main__':
    print("\n#1 Get user profile (GetItem on UserOrders)")
    profile = user.get_user_profile("aarchamb")
    print("  {0} <{1}>, addresses: {2}".format(
        profile['fullname'], profile['email'], ", ".join(profile['address'])))

    print("\n#2 Get all orders for a user (Query user_id + begins_with ORDER#)")
    for o in user.get_user_orders("tgrimes1"):
        show_order(o)

    print("\n#3 Get user profile + orders (one Query on the item collection)")
    for entry in user.get_user_with_orders("aarchamb"):
        print("  sk = {0}".format(entry['sk']))

    print("\n#4 Get line items for each of tgrimes1's orders (Query on OrderItems)")
    for o in user.get_user_orders("tgrimes1"):
        show_order(o)
        show_items(o['order_id'])

    print("\n#7 / #8 Ship aarchamb's first order and its items")
    first = user.get_user_orders("aarchamb")[0]
    order.update_order_status("aarchamb", first['order_id'], "Shipped")
    for i in order.get_order_items(first['order_id']):
        order.update_item_status(first['order_id'], i['item_id'], "Shipped")
    show_items(first['order_id'])

    print("\nGSI OrdersByStatus: aarchamb's 'Placed' orders")
    for o in order.get_orders_by_status("aarchamb", "Placed"):
        show_order(o)

    print("\nGSI OrdersByStatus: tgrimes1's 'Placed' orders dated 1-5 Feb 2024")
    for o in order.get_orders_by_status("tgrimes1", "Placed", "2024-02-01", "2024-02-05"):
        show_order(o)
