from flask import Flask, render_template, request, redirect
import os

from core.dbdriver import get_db, init_tables
from core import redisdriver

app = Flask(__name__)


# Init tables in db
init_tables()

@app.route('/')
def index():
	""" Index page
	  Show list of `asks`, and cheer count of each ask
	"""

	redis_client = redisdriver.get_client()
	dataset = []

	with get_db().cursor() as cursor :
		# Get data in `ask` only (not with cheer count)
		cursor.execute("SELECT * FROM `ask`")
		result = cursor.fetchall()

		success = True

		for id, message, ip_address, register_time in result :
			cached_cnt = redis_client.get('askhy:chearcnt_' + str(id))

			if cached_cnt == None :
				# Re-run query with count(*)
				success = False
				break
			else :
				print("Cache hit: " + str(id))
				dataset.append((id, message, ip_address, register_time, int(cached_cnt)))

	if not success :
		with get_db().cursor() as cursor :
			# Get data with cheer count
			print("Cache not exists. Create cache")
			
			cursor.execute("SELECT *, (SELECT COUNT(*) FROM `cheer` WHERE ask_id = ask.id) AS cheer_cnt FROM `ask`")
			result = cursor.fetchall()

			dataset = []

			for id, message, ip_address, register_time, cheer_cnt in result :
				cheer_cnt = int(cheer_cnt)
				dataset.append((id, message, ip_address, register_time, cheer_cnt))
				redis_client.set('askhy:chearcnt_' + str(id), cheer_cnt)


	return render_template('main.html',
		dataset=dataset,
	)


@app.route('/ask/<int:ask_id>', methods=['GET'])
def view_ask(ask_id):
	""" Show detail of one `ask`
	  See all cheers in this ask

	:param ask_id: Primary key of `ask` table
	"""
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


@app.route('/ask', methods=['POST'])
def add_ask():
	""" Add new ask

	:post-param message: Message of `ask`
	"""
	conn = get_db()
	message = request.form.get('message')

	with conn.cursor() as cursor :
		sql = "INSERT INTO `ask` (`message`, `ip_address`) VALUES (%s, %s)"
		r = cursor.execute(sql, (message, request.remote_addr))

	id = conn.insert_id()
	conn.commit()

	return redirect("/#a" + str(id))



@app.route('/ask/<int:ask_id>/cheer', methods=['POST'])
def add_cheer(ask_id):
	""" Add new cheer to ask

	:param ask_id: Primary key of `ask` table
	:post-param message: Message of `cheer`
	"""
	conn = get_db()
	message = request.form.get('message')

	with conn.cursor() as cursor :
		sql = "INSERT INTO `cheer` (`ask_id`, `message`, `ip_address`) VALUES (%s, %s, %s)"
		r = cursor.execute(sql, (ask_id, message, request.remote_addr))

	conn.commit()

	with conn.cursor() as cursor :
		cursor.execute("SELECT COUNT(*) FROM `cheer` WHERE ask_id = %s", (ask_id, ))
		row = cursor.fetchone()
		cheer_cnt = row[0]

		# Update cache
		redis_client = redisdriver.get_client()
		redis_client.set('askhy:chearcnt_' + str(ask_id), int(cheer_cnt))


	redirect_url = request.form.get('back', '/#c' + str(ask_id))
	return redirect(redirect_url)



@app.template_filter()
def hide_ip_address(ip_address):
	"""
	Template filter: <hide_ip_address>
	Hide last sections of IP address

	ex) 65.3.12.4 -> 65.3.*.*
	"""
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
