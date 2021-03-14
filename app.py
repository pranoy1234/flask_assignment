from flask import Flask, render_template, jsonify, request, redirect, flash, url_for ,send_from_directory
import mysql.connector
from datetime import datetime
import yaml

#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ parsing config.yaml @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

paths_yaml_file = open("./config.yaml")
parsed_yaml_file = yaml.load(paths_yaml_file, Loader=yaml.FullLoader)
user_name = parsed_yaml_file['config']['user']
password_user = parsed_yaml_file['config']['password']
host_ip = parsed_yaml_file['config']['host']
database_name = parsed_yaml_file['config']['database']

app = Flask(__name__)
def get_connection():
	#@@@@@@@@@@@@@@ Establishing connection with mysql Server  @@@@@@@@@
	try:
		mydb = mysql.connector.connect(user = user_name, password=password_user,host=host_ip,database=database_name )
		return mydb,True
	except Exception:
		return _,False

# @@@@@@@@@@@@@@@@@@@ Establishing connection @@@@@@@@@@@@@@@@@
mydb,status = get_connection()
mycursor = mydb.cursor()

# @@@@@@@@@@@@@@@@@@@ Create API  @@@@@@@@@@@@@@@@@
@app.route('/create_api',methods=['GET','POST'])
def create_api():
	data = request.get_json()
	
	if request.method == 'GET':
		return {'status':400}
	if status :
		if data['audioFileType'] not in ['song','podcast','audiobook']:
			return {'status':400}
		else:
			
			now = datetime.now()
			formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

			if data['audioFileType'] == 'song':
				try:
					mycursor.execute('insert into song(id,name,duration,upload_time) values(%s, %s,%s,%s)', (data['audioFileMetadata']['id'],data['audioFileMetadata']['name'],data['audioFileMetadata']['duration'],formatted_date))
				except Exception:
					return {'status':"500"}
				mydb.commit()
				return {'status':"200 OK"}

			elif data['audioFileType'] == 'podcast':
				try:
					mycursor.execute('insert into podcast(id,name,duration,host,upload_time) values(%s, %s,%s,%s,%s)', (data['audioFileMetadata']['id'],data['audioFileMetadata']['name'],data['audioFileMetadata']['duration'],data['audioFileMetadata']['host'],formatted_date))
				except Exception:
					return {'status':"500"}
				mydb.commit()
				return {'status':"200 OK"}

			elif data['audioFileType'] == 'audiobook':
				try:
					mycursor.execute('insert into audiobook(id,title,author,narrator,duration,upload_time) values(%s, %s,%s,%s,%s,%s)', (data['audioFileMetadata']['id'],data['audioFileMetadata']['title'],data['audioFileMetadata']['author'],data['audioFileMetadata']['narrator'],data['audioFileMetadata']['duration'],formatted_date))
				except Exception:
					return {'status':"500"}
				mydb.commit()
				return {'status':"200 OK"}


	else:
		return {'status':500}

# @@@@@@@@@@@@@@@@@@@ Delete API @@@@@@@@@@@@@@@@@
@app.route('/delete/<path:audioFileType>/<path:_id>',methods=['DELETE'])
def delete(audioFileType,_id):

	if audioFileType == "song":
		sql = "DELETE FROM song WHERE id = %s"
		try:
			mycursor.execute(sql, (_id,))
			mydb.commit()
			return {"status":"200 OK"}
		except Exception:
			return {"status":"500 "}

	elif audioFileType == "podcast":
		sql = "DELETE FROM podcast WHERE id = %s"
		try:
			mycursor.execute(sql, (_id,))
			mydb.commit()
			return {"status":"200 OK"}
		except Exception:
			return {"status":"500"}

	if audioFileType == "audiobook":
		sql = "DELETE FROM audiobook WHERE id = %s"
		try:
			mycursor.execute(sql, (_id,))
			mydb.commit()
			return {"status":"200 OK"}
		except Exception:
			return {"status":"500 "}
	return {"status":"500 "}

# @@@@@@@@@@@@@@@@@@@ Update API @@@@@@@@@@@@@@@@@
@app.route('/update/<path:audioFileType>/<path:_id>',methods=['GET','POST'])
def update(audioFileType,_id):

	data = request.get_json()
	now = datetime.now()
	formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
	if audioFileType == "song":
		sql = "UPDATE song SET name=%s,duration=%s,upload_time=%s  WHERE id = %s"
		try:
			mycursor.execute(sql, (data['audioFileMetadata']['name'],data['audioFileMetadata']['duration'],formatted_date,_id))
			mydb.commit()
			return {"status":"200 OK"}
		except Exception:
			return {"status":"500 "}

	if audioFileType == "podcast":
		sql = "UPDATE podcast SET name=%s,duration=%s,host=%s,upload_time=%s  WHERE id = %s"
		try:
			mycursor.execute(sql, (data['audioFileMetadata']['name'],data['audioFileMetadata']['duration'],data['audioFileMetadata']['host'],formatted_date,_id))
			mydb.commit()
			return {"status":"200 OK"}
		except Exception:
			return {"status":"500 "}

	if audioFileType == "audiobook":
		sql = "UPDATE audiobook SET title=%s,author=%s,narrator=%s,duration=%s,upload_time=%s  WHERE id = %s"
		try:
			mycursor.execute(sql, (data['audioFileMetadata']['title'],data['audioFileMetadata']['author'],data['audioFileMetadata']['narrator'],data['audioFileMetadata']['duration'],formatted_date,_id))
			mydb.commit()
			return {"status":"200 OK"}
		except Exception:
			return {"status":"500 "}

	return {"status":"500 "}

# @@@@@@@@@@@@@@@@@@@ GET API @@@@@@@@@@@@@@@@@
@app.route('/get/<path:audioFileType>/<path:_id>',methods=['GET','POST'])
def get_1(audioFileType,_id):
	out = {}
	if audioFileType == "song":
		try:
			sql = "SELECT * FROM song where id = %s"
			mycursor.execute(sql, (_id,))
			myresult = mycursor.fetchall()
			header = [i[0] for i in mycursor.description]
			for idx in range(len(header)):
				out[header[idx]] = myresult[0][idx]
			return {"data":out}
		except Exception:
			return {"status":"500"}

	if audioFileType == "podcast":
		try:
			sql = "SELECT * FROM podcast where id = %s"
			mycursor.execute(sql, (_id,))
			myresult = mycursor.fetchall()
			header = [i[0] for i in mycursor.description]
			for idx in range(len(header)):
				out[header[idx]] = myresult[0][idx]
			return {"data":out}
		except Exception:
			return {"status":"500"}

	if audioFileType == "audiobook":
		try:
			sql = "SELECT * FROM audiobook where id = %s"
			mycursor.execute(sql, (_id,))
			myresult = mycursor.fetchall()
			header = [i[0] for i in mycursor.description]
			for idx in range(len(header)):
				out[header[idx]] = myresult[0][idx]
			return {"data":out}
		except Exception:
			return {"status":"500"}



@app.route('/get/<path:audioFileType>',methods=['GET','POST'])
def get_2(audioFileType):
	out_in,out_out = {},[]
	if audioFileType == "song":
		try:
			sql = "SELECT * FROM song "
			mycursor.execute(sql)
			myresult = mycursor.fetchall()
			for j in range(len(myresult)):
				out_in = {}
				header = [i[0] for i in mycursor.description]
				for idx in range(len(header)):
					out_in[header[idx]] = myresult[j][idx]
				out_out.append(out_in)
			return {"data":out_out}
		except Exception:
			return {"status":"500"}

	if audioFileType == "podcast":
		try:
			sql = "SELECT * FROM podcast"
			mycursor.execute(sql)
			myresult = mycursor.fetchall()
			for j in range(len(myresult)):
				out_in = {}
				header = [i[0] for i in mycursor.description]
				for idx in range(len(header)):
					out_in[header[idx]] = myresult[j][idx]
				out_out.append(out_in)
			return {"data":out_out}
		except Exception:
			return {"status":"500"}

	if audioFileType == "audiobook":
		try:
			sql = "SELECT * FROM audiobook "
			mycursor.execute(sql)
			myresult = mycursor.fetchall()
			for j in range(len(myresult)):
				out_in = {}
				header = [i[0] for i in mycursor.description]
				for idx in range(len(header)):
					out_in[header[idx]] = myresult[j][idx]
				out_out.append(out_in)
			return {"data":out_out}
		except Exception:
			return {"status":"500"}
	

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.debug = True
    app.run(host='0.0.0.0',port = '4401')
