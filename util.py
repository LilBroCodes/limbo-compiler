import json
import logging
from colorlog import ColoredFormatter

class Logging:
   @staticmethod
   def change_log_format(name: str):
      logger = logging.getLogger(name)
      logger.setLevel(logging.DEBUG)

      formatter = ColoredFormatter(
         fmt='%(light_black)s%(asctime)s %(log_color)s%(levelname)-8s %(purple)s%(name)s: %(message_log_color)s%(message)s',
         datefmt='%Y-%m-%d %H:%M:%S',
         reset=True,
         log_colors={  # Controls only %(log_color)s (used around levelname)
            'DEBUG': 'cyan',
            'INFO': 'white',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
         },
         secondary_log_colors={  # Controls %(message_log_color)s (used around message)
            'message': {
               'DEBUG': 'bold_light_black',
               'INFO': 'white',
               'WARNING': 'yellow',
               'ERROR': 'red',
               'CRITICAL': 'bold_red',
            }
         },
         style='%'
      )

      logger.handlers.clear()

      handler = logging.StreamHandler()
      handler.setFormatter(formatter)
      logger.addHandler(handler)

      return logger

def serialize(obj: object, indent=0):
   obj_dict = obj.__dict__
   dict_str = str(obj_dict).strip().replace("'", '"')
   json_obj = json.loads(dict_str)
   return json.dumps(json_obj, indent=indent)
