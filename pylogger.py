
#=============================USER GUIDE==============================#
# STEP1: IMPORTING PYLOGGER
#    place the following code around top of module
#
#       from pylogger import get_logger
#       logger = get_logger()
#
# STEP2: HOW TO LOG
#   "ESSENTIALLY" Print statements that document our code
#   5 Levels of severity -- In a function (for example)
#       - DEBUG:    lowest, states what the function does
#       - INFO:     states what's expected of the function
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
#
#       result = divide(10, 2)
#       logger.info(f"Division result: {result}")
#       result = divide(10, 0)
#       logger.warning("Division operation failed")
#
#
# CRITICAL
#
#       Rarely happens, but when it does...
#                        ...something catastrophic happened!
#   Use for:
#       - A bug that causes the module to crash or become unusable
#       - Initialization failure (missing or corrupt config files)


# PYTHONS DOCUMENTATION
#   https://docs.python.org/3/howto/logging.html
#=====================================================================#
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

def send_order(logger, order):
    logger.debug(f'sending order: {order}')
    logger.debug(f'send order')

## Log Incoming and Outgoing Trades
##


