from views import BaseHandler
import logging as log
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.blobstore import BlobInfo
from google.appengine.api import images
from webapp2_extras import json
from google.appengine.api import mail
from utils import apiMethod, validateForm 
import csv, sys 
from webapp2_extras import json
from models.user import User

class Home(BaseHandler):
	def get(self):
		self.render_response("login.html")
	
	@validateForm([('email','email'),('password','password'),('dob','dateofbirth')])
	@apiMethod(User.create)
	def post(self):
		self.response.write("working")

#Signup
class Signup(BaseHandler):
	def get(self):
		self.render_response("signup.html")

	@validateForm([('email','email'),('password','password'),('dob','dateofbirth'),('phone','phone'),('first_name','notempty'),('last_name','string')])
	@apiMethod(User.create)
	def post(self):
		self.response.write("working")

#Login using email, password
class Login(BaseHandler):
	def get(self):
		self.render_response("login.html")

	@validateForm([('username','email'),('password','password')])
	@apiMethod(User.login)
	def post(self):
		self.response.write("working")

#Facebook Login
class FBLogin(BaseHandler):
	def get(self):
		pass

	@validateForm([('facebook_id','id')])
	@apiMethod(User.fblogin)
	def post(self):
		self.response.write("working")
		
#Twitter Login
class TLogin(BaseHandler):
	def get(self):
		pass

	@validateForm([('twitter_id','id')])
	@apiMethod(User.tlogin)
	def post(self):
		self.response.write("working")

class Pwdreset(BaseHandler):
	def get(self):
		pass

	@validateForm([('username','email'),('oldpwd','password'),('newpwd','password')])
	@apiMethod(User.pwdreset)
	def post(self):
		self.response.write("working")

class Forgotpwd(BaseHandler):
	def get(self):
		pass

	@validateForm([('email','email')])
	@apiMethod(User.forgotpwd)
	def post(self):
		self.response.write("working")
