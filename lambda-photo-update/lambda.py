import json
import pymongo
import os
import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def lambda_handler(event, context):
    logger.info("Received event: %s", json.dumps(event))

    try:
        # Parse the S3 event
        s3_bucket = event['Records'][0]['s3']['bucket']['name']
        s3_key = event['Records'][0]['s3']['object']['key']
        logger.info("S3 Bucket: %s", s3_bucket)
        logger.info("S3 Key: %s", s3_key)

        # MongoDB connection details
        mongo_host = os.environ['MONGO_HOST']
        mongo_port = int(os.environ['MONGO_PORT'])
        mongo_user = os.environ['MONGO_USER']
        mongo_pass = os.environ['MONGO_PASS']
        db_name = os.environ['DB_NAME']
        logger.info("MongoDB Host: %s", mongo_host)
        logger.info("MongoDB Port: %d", mongo_port)
        logger.info("Database Name: %s", db_name)

        # Connect to MongoDB
        client = pymongo.MongoClient(f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/")
        db = client[db_name]
        collection = db['photos']

        # Prepare the document to be inserted
        document = {
            "photo_name": s3_key,
            "upload_time": datetime.datetime.now()
        }

        # Insert the document into the MongoDB collection
        collection.insert_one(document)
        logger.info("Document inserted into MongoDB: %s", document)

        return {
            'statusCode': 200,
            'body': json.dumps('Success')
        }
    except Exception as e:
        logger.error("Error processing event: %s", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing event')
        }
