from flask import Flask, render_template, request, redirect
import os

from core.dbdriver import get_db, init_tables

app = Flask(__name__)


# Init tables in db
init_tables()

"""
Index page
Show list of `asks`, and cheer count of each ask
"""
@app.route('/')
def index():
	with get_db().cursor() as cursor :
		cursor.execute("SELECT *, (SELECT COUNT(*) FROM `cheer` WHERE ask_id = ask.id) AS cheer_cnt FROM `ask`")
		result = cursor.fetchall()

	return render_template('main.html',
		dataset=result,
	)


"""
Show detail of one `ask`
See all cheers in this ask
"""
@app.route('/ask/<int:ask_id>', methods=['GET'])
def view_ask(ask_id):
	conn = get_db()

	with conn.cursor() as cursor :
		cursor.execute("SELECT * FROM `ask` WHERE id = %s", (ask_id, ))
		row = cursor.fetchone()

		cursor.execute("SELECT * FROM `cheer` WHERE ask_id = %s", (ask_id, ))
		rows2 = cursor.fetchall()

	return render_template('detail.html',
		id=row[0],
		message=row[1],
		ip_address=row[2],
		register_time=row[3],
		current_url=request.url,
		cheers=rows2,
	)


"""
Add new ask

[request params]
  - message
"""
@app.route('/ask', methods=['POST'])
def add_ask():
	conn = get_db()
	message = request.form.get('message')

	with conn.cursor() as cursor :
		sql = "INSERT INTO `ask` (`message`, `ip_address`) VALUES (%s, %s)"
		r = cursor.execute(sql, (message, request.remote_addr))

	id = conn.insert_id()
	conn.commit()

	return redirect("/#a" + str(id))


"""
Add new cheer

[request params]
  - ask_id
  - message
"""
@app.route('/cheer', methods=['POST'])
def add_cheer():
	conn = get_db()
	ask_id = request.form.get('ask_id')
	message = request.form.get('message')

	with conn.cursor() as cursor :
		sql = "INSERT INTO `cheer` (`ask_id`, `message`, `ip_address`) VALUES (%s, %s, %s)"
		r = cursor.execute(sql, (ask_id, message, request.remote_addr))

	conn.commit()

	back = request.form.get('back')
	if back :
		return redirect(back)
	else :
		return redirect("/#c" + ask_id)


"""
Template filter: <hide_ip_address>
Hide last sections of IP address

ex) 65.3.12.4 -> 65.3.*.*
"""
@app.template_filter()
def hide_ip_address(ip_address):
	if not ip_address : return ""
	else :
		ipa = ip_address.split(".")
		return "%s.%s.*.*" % (ipa[0], ipa[1])




if __name__ == '__main__':
	app.run(
		host='0.0.0.0',
		debug=True,
		port=os.environ.get('APP_PORT', 8080)
	)
