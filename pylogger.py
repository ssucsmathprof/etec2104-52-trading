
#=============================USER GUIDE==============================#
# STEP1: IMPORTING PYLOGGER
#    place the following code around top of module
#
#       from pylogger import get_logger
#       logger = get_logger()
#
# STEP2: HOW TO LOG
#   "ESSENTIALLY" Print statements that document our code
#   5 Levels of severity
#       - DEBUG:    lowest, states what the function does
#       - INFO:     states whats expected of the function
#       - WARNING:  potential problem - function works
#       - ERROR:    problem happened - (a) function failed
#       - CRITICAL: highest(rare), Program has failed
#
# EXAMPLE
#
#       def divide(x, y):
#           logger.debug(f"Dividing {x} by {y}")
#           if y == 0:
#               logger.error("Attempted to divide by zero!")
#               return None
#           return x / y
#       result = divide(10, 2)
#       logger.info(f"Division result: {result}")
#       result = divide(10, 0)
#       logger.warning("Division operation failed"
#

# PYTHONS DOCUMENTATION
#   https://docs.python.org/3/howto/logging.html
#====================================================================#
import logging

file_handler = logging.FileHandler('trade.log') # print to file
console_handler = logging.StreamHandler()       # print to console

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s'        # time
                           ' - %(filename)s'    # module name
                           ' - %(funcName)s'    # containing function
                           ' - %(lineno)d'      # line number
                           ' - %(levelname)s'   # severity level
                           ' - %(message)s',    # your message
                    handlers=[file_handler, console_handler])

def get_logger():
    return logging.getLogger(__name__)


