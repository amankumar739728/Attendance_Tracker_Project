# importing module
import logging

# Create and configure logger
logging.basicConfig(filename="log_folder/newfile.log",
                    format='%(asctime)s - %(levelname)s -- %(filename)s - %(lineno)d - %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

# Test messages
logger.debug("Harmless debug Message")
logger.info("Just an information")
logger.warning("Its a Warning")
logger.error("Did you try to divide by zero")
logger.critical("Internet is down\n")


#output: A file named newfile.log will be created with the following content:
# 2025-05-09 15:59:54,049 Harmless debug Message
# 2025-05-09 15:59:54,050 Just an information
# 2025-05-09 15:59:54,050 Its a Warning
# 2025-05-09 15:59:54,050 Did you try to divide by zero
# 2025-05-09 15:59:54,050 Internet is down

import logging

logging.basicConfig(filename="log_folder/newfile.log",level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s',filemode='w')


def perform_operation(value):
    if value < 0:
        raise ValueError("Invalid value: Value cannot be negative.")
    else:
        # Continue with normal execution
        logger.info(f"Performing operation with value: {value}")
        logging.info("Operation performed successfully.")


try:
    input_value = int(input("Enter a value: "))
    perform_operation(input_value)
except ValueError as ve:
    logging.exception("Exception occurred: %s", str(ve))
    
    
#output:
# Enter a value: 5
# 2025-05-09 16:11:39,833 - INFO - Operation performed successfully.


