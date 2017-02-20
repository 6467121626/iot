#
# IOT E6756 Lab Assignment 3
#
# Group: JSJC - Jack Bott, Jingshi Chen, and Shuwei Feng
#
# Part 2 (60pts)
# Using the code you developed in Part 1, complete the Lab3/dynamodata.py file.
#
# You are required to have 2 tasks running in parallel (20pts for
# multithreading + 30pts for the functionality):
# a. The first task, running every 30 sec, shall look at adding data to the
# "mtadata" DynamoDB table continuously.
# b. A second task, running every 60 sec, looks at cleaning out data from the
# table that is older than 2 minutes old.
#
# This should be implemented on the Intel Edison first. Since this should
# really be implemented on a cloud service, you must also port your code to a
# cloud service, using AWS EC2-based Virtual Machines. You must demonstrate
# functionality on both platforms for full credit.

import json, time, threading
from collections import OrderedDict
from threading import Thread

import boto3
from boto3.dynamodb.conditions import Key,Attr

from utils import tripupdate,vehicle,alert,aws,mtaUpdates

# *********************************************************************************************
# Program to update dynamodb with latest data from mta feed. It also cleans up stale entried from db
# Usage python A3_2.py
# *********************************************************************************************


# Create DynamoDB item in existing database
def create_item(name, item):
    # name must be string
    # item must be dict
    try:
        # Get the service resource.
        dynamodb = aws.getResource('dynamodb', 'us-east-1')
        table = dynamodb.Table(name)
        table.put_item(Item=item)
        return True
    except KeyboardInterrupt:
        exit
    except:
        print "Error in Create Item"
        return False

# Batch create Items
def batch_create_item(name, item):
    try:
        # Get the service resource.
        dynamodb = aws.getResource('dynamodb', 'us-east-1')
        table = dynamodb.Table(name)
        with table.batch_writer() as batch:
            batch.put_item(Item=item)
        return True
    except KeyboardInterrupt:
        exit
    except:
        print "Error in Batch Create"
        return False

# Delete DynamoDB item in existing database mtaData
def delete_item(key):
    # name must be string
    # item must be dict
    try:
        # Get the service resource.
        dynamodb = aws.getResource('dynamodb', 'us-east-1')
        table = dynamodb.Table(name)
        table.delete_item(Key=key)
        return True
    except KeyboardInterrupt:
        exit
    except:
        print "Error in Delete Item"
        return False

# Search for timestamps less than input
def search_timestamp(ts):
    # inputs must be strings
    try:
        # Get the service resource.
        dynamodb = aws.getResource('dynamodb', 'us-east-1')
        table = dynamodb.Table(name)
        result = table.scan(timestamp__lt=ts)
        for n in result:
            print n
            #print n['timestamp']
        return
    except KeyboardInterrupt:
        exit
    except:
        print "Error in timestamp search"
        return False

# Initialize begining times for threads
b1, b2 = 0, 0

def add():
    print threading.currentThread().getName(), 'Starting'
    ts = time.time()
    item = {"tripId":1, "timestamp":str(ts)}
    create_item('mtaData', item)
    print threading.currentThread().getName(), 'Exiting'

def clean():
    print threading.currentThread().getName(), 'Starting'
    ts_clean = time.time()

    print threading.currentThread().getName(), 'Exiting'

print "Press Ctrl+C to escape..."
try:
    while True:
        if b1 == 0:
            b1 = time.time()
            print b1
            t1= threading.Thread(name='add new data', target=add) # Define Threads
            t1.start() # Start thread t1
        if b2 == 0:
            b2 = time.time()
            print b2
            t2= threading.Thread(name='clean old data', target=clean) # Define Threads
            t2.start() # Start thread t2
        if time.time() - b1 > 30:
            b1 = 0
        if time.time() - b2 > 60:
            b2 = 0
except KeyboardInterrupt:
    exit
except:
    print "Error"
