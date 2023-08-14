import logging
import pickle
From pathlib import Path

from daeploy import service
from daeploy.data_types import ArrayOutput,DataframeInput

logger = logging.getLogger(_name_)
THIS_DIR = Path(__file_).parent

with open(THIS_DIR/ "models/model_binary.dat.gz”, "rb") as fp:
   CLASSFIER = pickle.load (fp)


@service.entrypoint

def predict(data: DataFrameInput) -> ArrayOutput:
   logger.info(f"Recieved data: \n{data}")
   pred = CLASSIFIER.predict(data)
   logger.info(f"Predicted: {pred}")
   return pred

if__name__ == "_main_"
    service.run()
