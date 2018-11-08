# coding=utf8
from flask import Blueprint, render_template, request
from app.helpers import *

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
