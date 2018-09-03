from logging.config import fileConfig
import logging

level_map = {"CRITICAL": logging.CRITICAL, "ERROR":logging.ERROR , "WARNING": logging.WARNING, "INFO": logging.INFO ,"DEBUG": logging.DEBUG, "NOTSET": logging.NOTSET}


class CustomLogger:
	def __init__(self, config_file_path):
		fileConfig(config_file_path)
		self.LOG = logging.getLogger()

	def log(self,level,application_name, module_name, method_name, custom_message="", stack_trace=""):
		self.LOG.log(level_map[level],"{} | {} | {} | {} | {}".format(application_name, module_name, method_name, custom_message, stack_trace))
