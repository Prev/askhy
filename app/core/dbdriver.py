import pymysql
import os

_db_instance = None
def get_db() :
	""" Get database connection singleton object
	"""
	global _db_instance
	if _db_instance: return _db_instance
	else :
		_db_instance = pymysql.connect(
			host=os.environ.get('DATABASE_HOST', 'localhost'),
			user=os.environ.get('DATABASE_USER', 'root'),
			passwd=os.environ.get('DATABASE_PASS', ''),
			db=os.environ.get('DATABASE_NAME', 'test'),
			port=int(os.environ.get('DATABASE_PORT', 3306)),
			charset='utf8'
		)

		return _db_instance


def init_tables() :
	""" Init tables in this app
	"""
	with get_db().cursor() as cursor :
		try :
			cursor.execute("SELECT 1 FROM ask")
		except pymysql.err.ProgrammingError as e :
			from pymysql.constants import ER

			if e.args[0] == ER.NO_SUCH_TABLE :
				# Create tables
				cursor.execute("""
					CREATE TABLE IF NOT EXISTS `ask` (
					  `id` int(11) NOT NULL AUTO_INCREMENT,
					  `message` text COLLATE utf8mb4_unicode_ci NOT NULL,
					  `ip_address` varchar(30) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
					  `register_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
					  PRIMARY KEY (`id`)
					) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=1 ;

					CREATE TABLE IF NOT EXISTS `cheer` (
					  `id` int(11) NOT NULL AUTO_INCREMENT,
					  `ask_id` int(11) NOT NULL,
					  `message` text COLLATE utf8mb4_unicode_ci NOT NULL,
					  `ip_address` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT '',
					  `register_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
					  PRIMARY KEY (`id`),
					  KEY `ask_id` (`ask_id`)
					) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci AUTO_INCREMENT=1 ;

					ALTER TABLE `cheer`
			  			ADD CONSTRAINT `cheer_ibfk_1` FOREIGN KEY (`ask_id`) REFERENCES `ask` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
				""")

			else :
				raise e
			

		
