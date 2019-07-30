# coding=utf8
import shutil
from flask import Blueprint, render_template, request, send_from_directory, make_response
from app.helpers import *
import os
import zipfile
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

app_controller = Blueprint('app_controller', __name__, url_prefix='/')

'''
Dashboard
'''
@app_controller.route('', methods=['GET', 'POST'])
def dashboard():
	data = {"menuid": 1}
	return render_template("dashboard.html", data=data)

'''
DB tools
'''
@app_controller.route('dbtools', methods=['GET', 'POST'])
def db_tools():
	db_name = request.args.get('db_name')
	table_name = request.args.get('table_name')
	object_name = request.args.get('object_name')
	dbs = get_databases()
	if not db_name:
		db_name = dbs[0]
	tables = get_tables(db_name)
	if not table_name:
		table_name = tables[0]

	fields = get_table_field(db_name + '.' + table_name);

	insert_sql = ''
	update_sql = ''
	delete_sql = ''
	select_sql = ''
	simple_select_sql = ''
	java_code = ''
	java_mapper = ''
	java_service = ''
	mybatis_xml = ''
	test_case = ''

	if object_name:
		insert_sql = get_insert_sql(object_name, table_name, fields)
		update_sql = get_update_sql(object_name, table_name, fields)
		delete_sql = get_delete_sql(object_name, table_name, fields)
		select_sql = get_select_sql(table_name, fields)
		simple_select_sql = get_simple_select_sql(table_name, fields)
		java_code = get_java_code(object_name, fields)
		java_mapper = getJavaMapper(object_name, table_name, fields)
		java_service = getJavaService(object_name)
		mybatis_xml = get_mybatis_xml(object_name, table_name, fields)
		test_case = get_test_case(object_name)
	else:
		object_name = ''

	data = {"menuid": 2}
	return render_template("dbtools.html", data=data, dbs=dbs, tables=tables, db_name=db_name, table_name=table_name,
						   fields=fields, insert_sql=insert_sql, update_sql=update_sql, select_sql=select_sql,
						   simple_select_sql=simple_select_sql, delete_sql=delete_sql, java_code=java_code,
						   java_mapper=java_mapper, java_service=java_service,
						   mybatis_xml=mybatis_xml, object_name=object_name, test_case=test_case)

'''
DB tools download
'''
@app_controller.route('downloads', methods=['GET', 'POST'])
def downloads():
	db_name = request.args.get('db_name')
	table_name = request.args.get('table_name')
	object_name = request.args.get('object_name')
	dbs = get_databases()
	if not db_name:
		db_name = dbs[0]
	tables = get_tables(db_name)
	if not table_name:
		table_name = tables[0]

	fields = get_table_field(db_name + '.' + table_name);

	insert_sql = ''
	update_sql = ''
	delete_sql = ''
	select_sql = ''
	simple_select_sql = ''
	java_code = ''
	java_mapper = ''
	java_service = ''
	mybatis_xml = ''
	test_case = ''

	if object_name:
		java_code = get_java_codeStr(object_name, fields)
		java_mapper = getJavaMapperStr(object_name, table_name, fields)
		java_service = getJavaServiceStr(object_name)

		curr_dir = os.getcwd()
		path_entity = curr_dir + "\\entity"
		path_service = curr_dir + "\\service"
		path_mapper = curr_dir + "\\mapper"
		if os.path.exists(path_entity):
			shutil.rmtree(path_entity)
		os.makedirs(path_entity)
		if os.path.exists(path_service):
			shutil.rmtree(path_service)
		os.makedirs(path_service)
		if os.path.exists(path_mapper):
			shutil.rmtree(path_mapper)
		os.makedirs(path_mapper)
		file_path_entity = path_entity + "\\" + object_name + ".java"
		file_path_service = path_service + "\\" + object_name + "Service.java"
		file_path_mapper = path_mapper + "\\" + object_name + "Mapper.java"
		fp_entity = open(file_path_entity, "w")
		try:
			fp_entity.write(java_code.encode("utf-8"))
		finally:
			fp_entity.close()

		fp_service = open(file_path_service, "w")
		try:
			fp_service.write(java_service.encode("utf-8"))
		finally:
			fp_service.close()
		fp_mapper = open(file_path_mapper, "w")
		try:
			fp_mapper.write(java_mapper.encode("utf-8"))
		finally:
			fp_mapper.close()
		
		zip_pack = zipfile.ZipFile(object_name + ".zip", "w")
		zip_pack.write("entity" + "\\" + object_name + ".java")
		zip_pack.write("mapper" + "\\" + object_name + "Mapper.java")
		zip_pack.write("service" + "\\" + object_name + "Service.java")
		zip_pack.close()
		response = make_response(send_from_directory(curr_dir, object_name + ".zip", as_attachment=True))
		response.headers["Content-Disposition"] = "attachment; filename={}".format(object_name + ".zip".encode().decode('latin-1'))
		return response
	else:
		object_name = ''

	data = {"menuid": 2}
	return render_template("dbtools.html", data=data, dbs=dbs, tables=tables, db_name=db_name, table_name=table_name,
						   fields=fields, insert_sql=insert_sql, update_sql=update_sql, select_sql=select_sql,
						   simple_select_sql=simple_select_sql, delete_sql=delete_sql, java_code=java_code,
						   java_mapper=java_mapper, java_service=java_service,
						   mybatis_xml=mybatis_xml, object_name=object_name, test_case=test_case)
