import user_ops as user
import order_ops as order_ops   
from decimal import Decimal

if __name__ == '__main__':
    
    print(user.query_user_profile("tgrimes1"))
    
    orders = order_ops.query_user_orders("tgrimes1")

    for order in orders:
        order_id = order['sk'][7:] # Remove order prefix
        items = order_ops.query_order_items(order_id)
        print(items)
        for item in items:
            print(item['product_name'])
        
        