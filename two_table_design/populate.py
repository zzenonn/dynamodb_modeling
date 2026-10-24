#!/usr/bin/env python3
"""Load the same users and shopping carts as the Module 10 demo."""
from decimal import Decimal

import user_ops as user
import order_ops as order

if __name__ == '__main__':
    user.create_user("aarchamb", "Adam Archambault", "aarchambault0@wikipedia.org")
    user.add_address("aarchamb", "home", {
        "street": "1716 Fulton Lane",
        "state": "Csongrád",
        "country": "Hungary"
    })
    user.add_address("aarchamb", "office", {
        "street": "6 Manitowish Place",
        "state": "Csongrád",
        "country": "Hungary"
    })

    user.create_user("tgrimes1", "Trent Grimes", "tgrimes1@hostgator.com")
    user.add_address("tgrimes1", "home", {
        "street": "98905 Declaration Parkway",
        "country": "Honduras"
    })

    shopping_cart1 = [
        {'product_name': 'New Apple MacBook Pro',         'price': Decimal('2018.42'), 'quantity': 1},
        {'product_name': 'Nintendo Switch',               'price': Decimal('368.95'),  'quantity': 1},
        {'product_name': 'Seagate Portable 2TB External', 'price': Decimal('59.95'),   'quantity': 1},
    ]

    shopping_cart2 = [
        {'product_name': 'New Apple MacBook Pro',                          'price': Decimal('2018.42'), 'quantity': 1},
        {'product_name': 'Charmin Ultra Soft Cushiony Touch Toilet Paper', 'price': Decimal('0.49'),    'quantity': 10},
        {'product_name': 'The Legend of Zelda: Breath of the Wild',        'price': Decimal('74.94'),   'quantity': 1},
    ]

    shopping_cart3 = [
        {'product_name': 'HyperX Fury 16GB',            'price': Decimal('39.99'), 'quantity': 2},
        {'product_name': 'Jenga Classic Game',          'price': Decimal('19.99'), 'quantity': 1},
        {'product_name': "Tasha's Cauldron of Everything", 'price': Decimal('49.95'), 'quantity': 3},
    ]

    # Fixed dates so the date-range query in read_queries.py has
    # something to find.
    order.checkout("aarchamb", "home",   shopping_cart1, created_at="2024-01-15")
    order.checkout("aarchamb", "office", shopping_cart3, created_at="2024-01-20")
    order.checkout("tgrimes1", "home",   shopping_cart2, created_at="2024-02-01")
    order.checkout("tgrimes1", "home",   shopping_cart3, created_at="2024-02-10")
