import sys
from dataclasses import dataclass
#pipleline refers to a series of data processing steps that are chained together
#pipeline performs a specific task such as data cleaning, data transformation, feature extraction, model training and prediction
#
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer#for one hot encoding and standard scaling
from sklearn.impute import SimpleImputer#for handling missing values
from sklearn.pipeline import Pipeline#for creating pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder#for standard scaling and one hot encoding   

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"proprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformer_object(self):
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = ["gender", "race_ethnicity", "parental_level_of_education", "lunch", "test_preparation_course"]
            #for numerical features we are creating a pipeline
            num_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),#handling missing values replacing all the missing values with median
                    ('scaler', StandardScaler())#standard scaling
                ]
            )

            cat_pipeline = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent')),#handling missing values replacing all the missing values with mode
                    ('onehot', OneHotEncoder()),#one hot encoding
                    ("scalar", StandardScaler(with_mean=False))#standard scaling
                ]
            )

            logging.info("Numerical columns standard scaling completed")

            logging.info("Categorical columns encoding completed")

            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info("Read train and test data completed")

            logging.info("Obtaining preprocessing object")

            preprocessing_obj=self.get_data_transformer_object()

            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df=train_df.drop(columns=[target_column_name], axis=1)#creates a new feature dropping the target column(column we have to predict)
            target_feature_train_df=train_df[target_column_name]#extracts the target column
            #similar things happen for test data
            input_feature_test_df=test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info(
                f"Applying preprocessing object on training dataframe and testing dataframe."
            )

            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)#fits the preprocessing model
            #to the training data and transforms the training data(mean and standard deviation is calculated and then 
            # the data is transformed). It learns any parameters required to transform the data 
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)#transforming the testing data 
            #using transform . transform only applies transformation using the parameters learned during the fitting 
            # stage on the training data. It does not learn any new parameters from the test data

            train_arr = np.c_[#np.c is short form for numpy concatenate
                #input_feature_train_arr  is a numpy array containing the input features for training data
                input_feature_train_arr, np.array(target_feature_train_df)
            ]#new array where input feature and target feature are concatenated column-wise
            #suitable for training the model that requires input and target feature
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            #new array where the input features and the target feature(s) for 
            # the test data are concatenated column-wise, similar to the training data.
            
            logging.info(f"Saved preprocessing object.")
            #saving the pickle file
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (#contains tree tuples train_arr-> contains transformed training
                #dataset, after preprocessing steps like normalization, encoding etc
                train_arr,
                test_arr,#contains transformed testing dataset
                self.data_transformation_config.preprocessor_obj_file_path,#refers to the file path where a preprocessing object is saved
            )
        
        except Exception as e:
            raise CustomException(e,sys)