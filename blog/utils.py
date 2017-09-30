import os
from cms.models import *
def get_file_extension(filename):
	return os.path.splitext(filename)[-1][1:]


def contains_sensitive(published):
	count = 0
	words = Sensitive.objects.all()
	for i in words:
		count += published.count(i.words)
	if count > 0:
		return True
	else:
		return False