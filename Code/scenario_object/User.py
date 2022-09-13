class User:
	@staticmethod
	def receive_request(requestPackage):
		pass

	@staticmethod
	def send_request_package(requestPackage):
		print("User.send_request_package", requestPackage.get_request().get_id())