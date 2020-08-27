# DynamoDB Data Modeling Demo

To create a virtual environment run

`python3 -m venv ./.env`

Activate it with 

`source ./.env/bin/activate`

Install dependencies with

`pip install -r requirements.txt`
    
To close the environment when you're done, run `deactivate`

1. Run the `create_users_orders_table.py` first to create the table.
2. The `users_ops.py` file contains the functions related to users.
3. The `order_ops.py` file contains the functions related to orders.
4. Run the `populate.py` file will add records to the table
5. The `read_queries.py` will call the read functions from the other files