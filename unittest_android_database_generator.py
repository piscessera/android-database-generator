from android_database_generator import AndroidDatabaseGenerator
from build import Build
from android_database_generator import create_generate_dir
import filecmp
import os.path

import unittest

class TestSequenceFunctions(unittest.TestCase):

	def test_build_from_config_file_exist(self):
		config = Build()
		self.assertEqual(True, config.is_config_file_exist())

	def test_build_from_config_file_value(self):
		config = Build()
		self.assertEqual("com.piscessera.gen", config.get_pkg_name())
		self.assertEqual("gen_db", config.get_db_name())

	def test_pkg_exist(self):
		# make sure the package is added in function
		db = AndroidDatabaseGenerator()
		db.set_pkg("com.piscessera.gen")
		self.assertEqual("com.piscessera.gen", db.get_pkg())

	def test_gen_folder_exist(self):
		gen = AndroidDatabaseGenerator()
		self.assertEqual(True, os.path.exists("gen"))		

	def test_gen_core(self):
		gen = AndroidDatabaseGenerator()
		gen.generate()
		result = filecmp.cmp("DatabaseCore.test.java", "gen/database/DatabaseCore.java")
		self.assertEqual(True, result)

if __name__ == '__main__':
		unittest.main()