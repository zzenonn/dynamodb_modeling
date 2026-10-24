# Two-Table Design: UserOrders + OrderItems

This folder is the redesign from Module 11 (DynamoDB Design Patterns). Module 10's single table (`users-orders-items`) is split by access correlation:

- **UserOrders**: user profiles and their orders. Partition key `user_id`, sort key `sk` (`PROFILE` or `ORDER#<order_id>`).
  - GSI **OrdersByStatus**: partition key `user_id`, multi-attribute sort key `status` + `created_at`.
- **OrderItems**: line items. Partition key `order_id`, sort key `item_id`. Each item carries a copy of `product_name`.

## Access patterns

1. Get user profile: `user_ops.get_user_profile` (GetItem)
2. Get all orders for a user: `user_ops.get_user_orders` (Query, `begins_with ORDER#`)
3. Get user profile + orders: `user_ops.get_user_with_orders` (one Query on the item collection)
4. Get line items for an order: `order_ops.get_order_items` (Query on OrderItems)
5. Create a user: `user_ops.create_user`
6. Place an order: `order_ops.checkout` (one transaction across both tables)
7. Update order status: `order_ops.update_order_status`
8. Update item status: `order_ops.update_item_status`

There is also `order_ops.get_orders_by_status`, which queries the GSI by status with an optional date range.

## Running it

The tables are created in Singapore (`ap-southeast-1`). To use another region, change `REGION` in `create_tables.py`.

From this folder, with AWS credentials configured:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python create_tables.py   # creates both tables and waits until they are ready
python populate.py        # same users and carts as the Module 10 demo
python read_queries.py    # runs each access pattern and prints the results
python delete_tables.py   # removes both tables when you are done
```

Run `deactivate` to leave the virtual environment.
