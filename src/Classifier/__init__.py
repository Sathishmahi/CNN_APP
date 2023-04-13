import logging 
import os
import sys


log_dir="logs"
os.makedirs(log_dir,exist_ok=True)
log_file_path=os.path.join(
    log_dir,
    "running_logs.log"
)
format="[ %(asctime)s    %(levelname)   s%(module)s ]  [ %(message)s ]"
logging.basicConfig(
level=logging.INFO,
format=format,
handlers=[
    logging.FileHandler(log_file_path),
    # logging.StreamHandler(sys.stdout)
]
)
logger=logging.getLogger("ClassifierLogger")
