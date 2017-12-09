from flask import Flask, render_template, request, redirect
import os

from core.dbdriver import get_db, init_tables
from core import arcusdriver

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'


app = Flask(__name__)


# Init tables in db
init_tables()

@app.route('/')
def index():
	""" Index page
	  Show list of `asks`, and cheer count of each ask
	"""
	arcus_client = arcusdriver.get_client()
	dataset = []

	with get_db().cursor() as cursor :
		# Get data in `ask` only (not with cheer count)
		cursor.execute("SELECT * FROM `ask`")
		result = cursor.fetchall()

		success = True

		for id, message, ip_address, register_time in result :
			cache = arcus_client.get('askhy:cheercnt_' + str(id)).get_result()
			cache2 = arcus_client.get('askhy:cheercntp_' + str(id)).get_result()

			if cache == None or cache2 == None :
				# Re-run query with count(*)
				success = False
				break
			else :
				print(bcolors.OKGREEN + "Cache hit: " + str(id) + bcolors.ENDC)
				dataset.append((id, message, ip_address, register_time, cache, cache2))
		
	if not success :
		with get_db().cursor() as cursor :
			# Get data with cheer count
			print(bcolors.WARNING + "Cache not exists. Create cache" + bcolors.ENDC)
			
			cursor.execute("""SELECT *,
				(SELECT COUNT(*) FROM `cheer` WHERE ask_id = ask.id) AS cheer_cnt,
				(SELECT COUNT(DISTINCT ip_address) FROM `cheer` WHERE ask_id = ask.id) AS cheer_cnt_pure
				FROM `ask`
			""")
			result = cursor.fetchall()

			dataset = []

			for id, message, ip_address, register_time, cheer_cnt, cheer_cnt_pure in result :
				dataset.append((id, message, ip_address, register_time, cheer_cnt, cheer_cnt_pure))
				arcus_client.set('askhy:cheercnt_' + str(id), cheer_cnt)
				arcus_client.set('askhy:cheercntp_' + str(id), cheer_cnt_pure)


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

	ultra = request.form.get('ultra')


	def run() :
		with conn.cursor() as cursor :
			sql = "INSERT INTO `cheer` (`ask_id`, `message`, `ip_address`) VALUES (%s, %s, %s)"
			r = cursor.execute(sql, (ask_id, message, request.remote_addr))

		conn.commit()

		# Update cache
		with conn.cursor() as cursor :
			cursor.execute("SELECT COUNT(*), COUNT(DISTINCT ip_address) FROM `cheer` WHERE ask_id = %s", (ask_id, ))
			row = cursor.fetchone()
			cheer_cnt = row[0]
			cheer_cnt_pure = row[1]

			arcus_client = arcusdriver.get_client()
			arcus_client.set('askhy:cheercnt_' + str(ask_id), cheer_cnt)
			arcus_client.set('askhy:cheercntp_' + str(ask_id), cheer_cnt_pure)

	if ultra :
		for i in range(0, 100) :
			run()
	else :
		run()

	redirect_url = request.form.get('back', '/#c' + str(ask_id))
	return redirect(redirect_url)



@app.route('/ask/<int:ask_id>/cheer_trick')
def cheer_trick(ask_id):
	""" Add tricky cheers
	"""
	conn = get_db()
	message = '응원합니다!'
	
	with conn.cursor() as cursor :
		for i in range(0, 1000) :
			sql = "INSERT INTO `cheer` (`ask_id`, `message`, `ip_address`) VALUES (%s, %s, %s)"
			r = cursor.execute(sql, (ask_id, message, request.remote_addr))

	# Remove cache
	arcus_client = arcusdriver.get_client()
	arcus_client.delete('askhy:cheercnt_' + str(ask_id))
	arcus_client.delete('askhy:cheercntp_' + str(ask_id))

	conn.commit()
	return "success"


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
		port=os.environ.get('APP_PORT', 8081)
	)
