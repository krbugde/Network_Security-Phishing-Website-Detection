# Import os module to access environment variables and interact with the operating system
import os

# Import sys module to get system-level information (used in error handling)
import sys

# Import json module to convert data into JSON format
import json

# Import load_dotenv function from python-dotenv library
# This helps us load secret credentials stored in a .env file
from dotenv import load_dotenv

# Load all variables from the .env file into the environment
# After this line, we can access .env variables using os.getenv()
load_dotenv()

# Get the MongoDB connection URL from the .env file
# This URL contains the username, password, and cluster info to connect to MongoDB
# Example: mongodb+srv://username:password@cluster.mongodb.net/
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

# Import certifi library
# certifi provides SSL certificates to make secure HTTPS connections
import certifi

# Get the path to the SSL certificate file
# This is used to verify the identity of MongoDB server (security purpose)
ca = certifi.where()

# Import pandas to read and manipulate CSV files (like Excel but in Python)
import pandas as pd

# Import numpy for numerical operations (not directly used here but good practice)
import numpy as np

# Import pymongo to connect and interact with MongoDB database
import pymongo

# Import our custom exception class to handle errors in a detailed way
# It shows file name + line number + error message when something goes wrong
from networksecurity.exception.exception import CustomException

# Import our custom logger to record events/activities in a log file
from networksecurity.logging.logger import logging


# Define a class to handle all MongoDB data operations
# This class will: read CSV → convert to JSON → insert into MongoDB
class NetworkDataExtract:

    # Constructor: runs automatically when object is created
    # Currently does nothing (pass) but wrapped in try-except for safety
    def __init__(self):
        try:
            pass  # No initialization needed right now
        except Exception as e:
            # If any error occurs, raise our detailed CustomException
            raise CustomException(e, sys)

    # Method to convert CSV file data into JSON format
    # file_path → location of the CSV file to read
    def cv_to_json_convertor(self, file_path):
        try:
            # Read the CSV file and store it as a DataFrame (like a table)
            data = pd.read_csv(file_path)

            # Reset the index (row numbers) and drop the old index column
            # inplace=True means changes are applied directly to 'data'
            data.reset_index(drop=True, inplace=True)

            # Convert DataFrame to JSON format:
            # data.T → Transpose the data (flip rows and columns)
            # .to_json() → Convert to JSON string
            # json.loads() → Parse JSON string into Python dictionary
            # .values() → Get all records as a list of dictionaries
            records = list(json.loads(data.T.to_json()).values())

            # Return the list of records in JSON format
            return records

        except Exception as e:
            # If any error occurs, raise our detailed CustomException
            raise CustomException(e, sys)

    # Method to insert records into MongoDB database
    # records → list of JSON records to insert
    # database → name of the MongoDB database
    # collection → name of the MongoDB collection (like a table in SQL)
    def insert_data_to_mongodb(self, records, database, collection):
        try:
            # Store the database name in the object
            self.database = database

            # Store the collection name in the object
            self.collection = collection

            # Store the records in the object
            self.records = records

            # Create a connection to MongoDB using the URL from .env file
            # ca → SSL certificate for secure connection
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)

            # Select the database from MongoDB
            # If it doesn't exist, MongoDB will create it automatically
            self.database = self.mongo_client[self.database]

            # Select the collection (table) from the database
            # If it doesn't exist, MongoDB will create it automatically
            self.collection = self.database[self.collection]

            # Insert all records into the MongoDB collection at once
            self.collection.insert_many(self.records)

            # Return the total number of records inserted
            return len(self.records)

        except Exception as e:
            # If any error occurs, raise our detailed CustomException
            raise CustomException(e, sys)


# This block runs only when this file is executed directly
# It will NOT run if this file is imported in another file
if __name__ == '__main__':

    # Path to the CSV file containing phishing data
    FILE_PATH = "Network_Data\phisingData.csv"

    # Name of the MongoDB database where data will be stored
    DATABASE = "KUMUDINI"

    # Name of the MongoDB collection (like a table) where data will be stored
    Collection = "NetworkData"

    # Create an object of NetworkDataExtract class
    networkobj = NetworkDataExtract()

    # Convert the CSV file to JSON records using our method
    records = networkobj.cv_to_json_convertor(file_path=FILE_PATH)

    # Print the records to see what was extracted from the CSV
    print("Records=", records)

    # Insert the records into MongoDB and get the count of inserted records
    no_of_records = networkobj.insert_data_to_mongodb(records, DATABASE, Collection)

    # Print how many records were successfully inserted into MongoDB
    print("No of records: ", no_of_records)