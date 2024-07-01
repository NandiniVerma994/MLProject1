import sys#any exception that is gettin controlled this sys library will have the info
from src.logger import logging
#whenever an exception is raised, i want to push it on my own custom msg

#how the error message will look inside your file
def error_message_detail(error, error_detail:sys):
    _,_,exc_tb=error_detail.exe_info()#this will give me the error line number and the file name
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name,exc_tb.tb_lineno,str(error))

    return error_message
    



class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)

    def __str__(self):
        return self.error_message
    


