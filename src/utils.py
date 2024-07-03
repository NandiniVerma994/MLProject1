import numpy as np
import pandas as pd
import os
import sys
import dill

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