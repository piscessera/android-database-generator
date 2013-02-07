import os.path

class Build:
	global CONFIG_NAME

	def __init__(self):
		CONFIG_NAME = "build.config"
		self.pkg_name = ""
		self.db_name = ""
		# set default value to file flag variable is exist
		self.config_file_exist = os.path.exists("build.config")

		# if config file not exist, exit program and print some text..
		if not self.config_file_exist:
			print("build.config is not found!!\n")
			print("Please, create build.config\n")
			return

		# open file operator
		config_file = open("build.config")
		# read line in file
		for line in config_file.readlines():
			# split value with '=' for gethering key and value
			values = line.split("=")
			# check key is 'package_name'
			if values[0] == "package_name":
				# set package name value
				# rstrip is remove '\n' in value
				self.pkg_name = values[1].rstrip("\n")
			# check key is 'database name'
			if values[0] == "db_name":
				# set database name value
				# rstrip is remove '\n' in value
				self.db_name = values[1].rstrip("\n")
		# close file operator
		config_file.close()

	def get_pkg_name(self):
		return self.pkg_name

	def get_db_name(self):
		return self.db_name

	def is_config_file_exist(self):
		# return config file flag variable
		return self.config_file_exist