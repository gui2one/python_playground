from multiprocessing.managers import BaseManager
manager = BaseManager(address=('localhost', 50000), authkey='abc')
server = manager.get_server()
server.serve_forever()



# import SimpleXMLRPCServer

# def add(x,y):
# 	return x+y


# server = SimpleXMLRPCServer.SimpleXMLRPCServer(('localhost',8080))
# server.register_function(add)
# server.register_introspection_functions()



# print server
# server.serve_forever()