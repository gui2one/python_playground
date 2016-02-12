from multiprocessing.managers import BaseManager
m = BaseManager(address=('127.0.0.1', 5000), authkey='abc')
m.connect()


# import xmlrpclib

# client = xmlrpclib.ServerProxy('http://localhost:8080')
# print client.system.listMethods()
