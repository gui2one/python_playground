from termcolor import colored
from colorama import init

init()

import xmlrpclib

server = xmlrpclib.ServerProxy("http://localhost:5000")


success = server.getSucceededStatusNames()
failed = server.getFailedJobStatusNames()

for job in success:
	print (colored(job,"grey","on_green"))

for job in failed:
	print (colored(job,"grey","on_red"))