#!/usr/bin/env python3
import boto3
        
def delete_table(name):
    dynamodb = boto3.resource('dynamodb')  
    table = dynamodb.Table(name)
    table.delete()

if __name__ == '__main__':
    delete_table("users-orders-items")
