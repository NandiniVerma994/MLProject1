import numpy as np
import pandas as pd
import os
import sys
import dill


from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException
#save object is defined in the data transformation 
#it will take the file path and object makes directory
#opens the file , dill help us to create a pickle file
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)

        os.makedirs(dir_path, exist_ok=True)

        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        raise CustomException(e, sys)
    
def evaluate_models(X_train,y_train,X_test,y_test,models):
    try:
        report={}

        for i in range(len(list(models))):
            model = list(models.values())[i]#iterating over each and every model one by one
            # para = param[list(models.keys())[i]]#iterating over each and every parameter of the model

            # gs = GridSearchCV(model, para, cv=3)#grid search cv is used to find the best parameter of the model
            # gs.fit(X_train, y_train)#fitting the model on the training data
            # #after selecting the best model
            # model.set_params(**gs.best_params_)#setting the best parameter of the model
            # model.fit(X_train, y_train)#train model

            model.fit(X_train, y_train)#train model

            y_train_pred = model.predict(X_train)#predict on X_train data

            y_test_pred = model.predict(X_test)#predict on test data
            #The purpose of this line is to evaluate how well the model has
            #  learned from the training data by comparing these predictions
            #  (y_train_pred) against the actual outcomes (y_train
            train_model_score = r2_score(y_train, y_train_pred)#r2 score on train data

            test_model_score = r2_score(y_test, y_test_pred)#r2 score on test data  

            report[list(models.keys())[i]] = test_model_score#storing the r2 score of each model in the report dictionary

        return report
    
    except Exception as e:
        raise CustomException(e, sys)
    #Loading the pkl file
def load_object(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)