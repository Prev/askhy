from lib.arcus import *
from lib.arcus_mc_node import ArcusMCNodeAllocator, EflagFilter
import os

timeout = 20

""" Get acrus connection singleton object
"""
_arcus_client = None

def get_client() :
	global _arcus_client
	if _arcus_client: return _arcus_client
	else :
		_arcus_client = Arcus(ArcusLocator(ArcusMCNodeAllocator(ArcusTranscoder())))
		_arcus_client.connect(
			os.environ.get('ARCUS_URL', '127.0.0.1:2183'),
			os.environ.get('ARCUS_SERVICE_CODE', 'ruo91-cloud'),
		)

		return _arcus_client

