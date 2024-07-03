import sys#any exception that is gettin controlled this sys library will have the info
from src.logger import logging
#whenever an exception is raised, i want to push it on my own custom msg

#how the error message will look inside your file
def error_message_detail(error, error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()#this will give me the error line number and the file name
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
    
# if __name__ == "__main__":

#     try:
#         a=1/0
#     except Exception as e:
#         logging.info("Divide by Zero")
#         raise CustomException(e,sys)
    

'''This Python code snippet is designed to handle exceptions in 
a structured way, providing detailed error messages that include 
the script name, line number, and error message.
 error_message_detail function: This function is designed to format
   and return a detailed error message when an exception occurs. It 
   takes two parameters: error, which is the exception object, and 
   error_detail, which is expected to be a module that presumably 
   has an exe_info() method (likely a typo for sys.exc_info() from
     the sys module). The function extracts the traceback object
       from error_detail, then retrieves the filename and the line 
       number where the exception occurred. It formats these details
         into a string that includes the script name, line number, 
         and the error message, and returns this string.'''
