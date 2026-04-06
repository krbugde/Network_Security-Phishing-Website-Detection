from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging

## configuration of the Data Ingestion Config

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

from networksecurity.entity.artifact_entity import DataIngestionArtifact
import os
import sys
import numpy as np
import pandas as pd
import pymongo
from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")

import certifi
ca = certifi.where()

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except CustomException as e:
            raise CustomException(e,sys)
        
    def export_collection_as_dataframe(self):
        """
        Define a function named 'export_collection_as_dataframe'. 
        'def' is the Python keyword to define a function.
        'self' is a reference to the instance of the class that this method belongs to.
        This function will read data from a MongoDB collection and return it as a Pandas DataFrame.
        """

        try:
            # 'try' keyword is used to start a block of code where we anticipate exceptions/errors may occur.
            
            database_name = self.data_ingestion_config.database_name
            # 'database_name' is a variable to store the name of the MongoDB database.
            # 'self' refers to the current instance of the class.
            # 'data_ingestion_config' is an object/attribute of the class that holds configuration details.
            # 'database_name' inside 'data_ingestion_config' contains the name of the database we want to connect to.

            collection_name = self.data_ingestion_config.collection_name
            # 'collection_name' is a variable storing the name of the MongoDB collection.
            # A collection in MongoDB is like a table in SQL databases.

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)
            # 'self.mongo_client' stores the MongoDB client object.
            # 'pymongo.MongoClient()' is a function from the pymongo library to connect to MongoDB.
            # 'MONGO_DB_URL' is a variable (probably a constant) storing the MongoDB connection string.
            # This line connects Python to the MongoDB server.

            collection = self.mongo_client[database_name][collection_name]
            # Access the specific collection from the MongoDB database.
            # 'self.mongo_client[database_name]' gets the database.
            # '[collection_name]' accesses the specific collection inside the database.
            # 'collection' now holds a reference to the MongoDB collection we want to read from.

            df = pd.DataFrame(list(collection.find()))
            # 'df' is a variable storing the data as a Pandas DataFrame.
            # 'collection.find()' is a pymongo method that retrieves all documents from the collection.
            # 'list(...)' converts the cursor returned by 'find()' into a Python list of dictionaries.
            # 'pd.DataFrame(...)' converts the list of dictionaries into a DataFrame (tabular structure).
            # 'pd' refers to the 'pandas' library, used for data manipulation and analysis.

            if "_id" in df.columns.to_list():
                # Check if the '_id' column exists in the DataFrame.
                # '_id' is automatically added by MongoDB as a unique identifier for each document.
                # 'df.columns' returns the column names of the DataFrame.
                # '.to_list()' converts column names from Index object to a Python list.

                df = df.drop(columns=["_id"], axis=1)
                # Drop the '_id' column from the DataFrame.
                # 'df.drop()' is a pandas method to remove rows or columns.
                # 'columns=["_id"]' specifies which column to drop.
                # 'axis=1' means we are dropping a column (axis=0 would drop rows).

            df.replace({"na": np.nan}, inplace=True)
            # Replace all occurrences of the string "na" with 'NaN' (Not a Number) which pandas uses for missing values.
            # 'df.replace()' is a pandas method to replace values in a DataFrame.
            # '{"na": np.nan}' is a dictionary mapping: replace "na" with np.nan.
            # 'np.nan' is a NumPy object representing missing values.
            # 'inplace=True' means the replacement happens in the original DataFrame without creating a new one.

            return df
            # Return the final DataFrame 'df' to the caller.

        except Exception as e:
            # 'except' keyword is used to catch exceptions that occur inside the try block.
            # 'Exception as e' catches any type of error and assigns it to variable 'e'.

            raise CustomException(e, sys)
            # Raise a custom exception (defined elsewhere in your code) with the caught error 'e' and system info 'sys'.
            # 'CustomException' is likely a user-defined class to handle exceptions in a structured way.
            # 'sys' is the Python system module, usually used to get info about the error and traceback.

        
    def export_data_into_feature_store(self,data_frame:pd.DataFrame):
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            # creating folder
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            data_frame.to_csv(feature_store_file_path,index=False,header=True)
            return data_frame
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def split_data_as_train_test(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(
                dataframe,test_size=self.data_ingestion_config.train_test_split_ratio
            )

            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )  

            dir_path= os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info(f"Exporting train and test file path.")

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.test_file_path, index=False, header=True
            )
            logging.info(f"Exported train and test file path.")

            
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_ingestion(self):
        try:
            dataFrame=self.export_collection_as_dataframe()
            dataFrame=self.export_data_into_feature_store(dataFrame)
            self.split_data_as_train_test(dataFrame)
            dataingestionartifact=DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                        test_file_path=self.data_ingestion_config.test_file_path)
            return dataingestionartifact
        
        except Exception as e:
            raise CustomException(e,sys)