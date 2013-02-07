import os.path
import shutil
import sqlite3
import re
from build import Build

class AndroidDatabaseGenerator:

	def __init__(self):
		self.pkg_name = ""
		# call remove gen folder when starting generator module
		# remove_gen_folder()
		# create new gen folder
		create_generate_dir("gen")
		create_generate_dir("gen/database")
		create_generate_dir("gen/domain")

	def set_pkg(self, name):
		self.pkg_name = name

	def get_pkg(self):
		return self.pkg_name

	def generate(self):
		print("Start generate file..")
		build = Build()
		# open 
		core_tpl = open("template/DatabaseCore.java.tpl")
		core_new = []
		for line in core_tpl:
			# set package name
			line = line.replace("CONFIG_PKG_NAME", build.get_pkg_name())
			# set db name
			line = line.replace("CONFIG_DB_NAME", build.get_db_name())
			core_new.append(line)
		# close file
		core_tpl.close()
		# w+ is create new file, if file not exist
		core = open("gen/database/DatabaseCore.java", "w+")
		for line in core_new:
			core.write(line)
		core.close()
		print("End generate new file..")
		print("Prepare to generate database helper file..")

		db = SQLiteDatabase()
		cur_tbl = db.connect(build.get_db_name())
		cur_tbl.execute(db.get_database_structure_sql())
		for row in cur_tbl:
			# genereate core file
			if row[0] != "sqlite_sequence" and row[0] != "android_metadata":
				cur_col = db.connect(build.get_db_name())
				cur_col.execute(db.get_table_schema_sql(row[0]))
				sql = cur_col.fetchone()
				p = re.compile(r'"(.*?)"')
				# find value in quote by regex
				m = p.findall(sql[0])
				# create class name
				cls_name = row[0].replace("_", " ")
				cls_name = cls_name.title()
				cls_name = cls_name.replace(" ", "")
				# create domain file
				domain = open("gen/domain/"+cls_name+".java", "w+")
				domain.write("package " + build.get_pkg_name() + ".domain")
				domain.write("\n")
				domain.write("\n")
				domain.write("public class "+cls_name+" {")
				domain.write("\n")
				domain.write("\n")
				# loop for creating column variable
				for tbl in m:
					if tbl != row[0]:
						domain.write("public static final String " + tbl.upper() + " = \" " + tbl + " \";\n")

				# clean sql to normal form
				col_datatype = sql[0].replace("CREATE TABLE", "")
				col_datatype = col_datatype.replace("PRIMARY KEY", "")
				col_datatype = col_datatype.replace("AUTOINCREMENT", "")
				col_datatype = col_datatype.replace("NOT NULL", "")
				col_datatype = col_datatype.replace("UNIQUE", "")
				col_datatype = col_datatype.replace(row[0], "")
				col_datatype = col_datatype.replace("(", "")
				col_datatype = col_datatype.replace(")", "")
				col_datatype = col_datatype.replace("\"", "")
				col_datatype = col_datatype.replace(" ", "")
				col_datatype_list = col_datatype.split(",")
				
				domain.write("\n")
				variable = ""
				get_str = ""
				set_str = ""
				index = 1
				for datatype in col_datatype_list:
					variable += "private "
					get_str += "public "
					set_str += "public "
					# clean datatype
					datatype = datatype.replace(m[index], "")
					# variable
					variable += get_datatype_str(datatype) + " "
					variable += m[index]+";\n"

					method_name = m[index]
					if method_name[0] != "_":
						method_name = m[index].replace("_", " ")
						method_name = method_name.title()
						method_name = method_name.replace(" ", "")

					# get
					get_str += get_datatype_str(datatype) + " " + "get"
					get_str += method_name + " { return this." 
					get_str += m[index] + "; } \n"
					# set
					set_str += "void set" + method_name + "(" + get_datatype_str(datatype)  + " " 
					set_str += m[index] + "){ this." + m[index] + " = " + m[index] + "; }\n"
					index = index + 1

				domain.write(variable)
				domain.write("\n")
				domain.write(get_str)
				domain.write("\n")
				domain.write(set_str)
				domain.write("\n")
				domain.write("}")
						
				
		db.close()

def get_datatype_str(datatype):
	result = ""
	if datatype.lower() == "integer":
		result = "int"
	if datatype.lower() == "varchar":
		result = "String"
	if datatype.lower() == "double":
		result = "double"
	return result

def create_generate_dir(dir_name):
		if not os.path.exists(dir_name): 
			# create gen folder
			os.makedirs(dir_name)

def remove_gen_folder():
		if os.path.exists("gen"):
			# remove gen folder
		 	shutil.rmtree("gen")

class SQLiteDatabase:

	def connect(self, db_name):
		self.conn = sqlite3.connect(db_name+".sqlite")
		# return cursor for traveling in database
		return self.conn.cursor()

	def get_database_structure_sql(self):
		return "select name from sqlite_master where type = 'table'"

	def get_table_schema_sql(self, table_name):
		return "select sql from sqlite_master where type = 'table' and name = '"+table_name+"' "

	def close(self):
		self.conn.close()