import datetime
import logging as log
from google.appengine.ext import db
from formencode import validators
from datetime import datetime
from google.appengine.api import mail
from google.appengine.api import users


class User(db.Model):
	first_name = db.StringProperty() 
	last_name = db.StringProperty() 
	email = db.StringProperty() 
	password = db.StringProperty() 
	date_of_birth = db.DateTimeProperty()
	phone = db.PhoneNumberProperty()
	facebook_id = db.StringProperty()
	twitter_id = db.StringProperty()
	activation_code = db.StringProperty()
	

	@classmethod
	def create(cls,request,data,**kwargs):
		email =	data['email']
		password = data['password']
		d = data['dob']
		phone = data['phone']
		first_name = data['first_name']
		last_name = data['last_name']
		q = db.GqlQuery("SELECT * from User where email = :1",email)
		a = q.get()
		phone_duplicate = db.GqlQuery("SELECT * from User where phone = :1",phone).get()
		dob = validators.DateConverter(month_style = 'dd/mm/yyyy').to_python(d)
		time = validators.TimeConverter(use_datetime = True).to_python("0:0")
		dob = datetime.combine(dob,time)
		log.info("================================")
		log.info(a)
		log.info("================================")
		if phone_duplicate is not None:
			resp = {"status":False,"message":"phone number already exists","flawless_userid":str(phone_duplicate.key())}
			return resp 
		if a is not None:
			resp = {"status":False,"message":"email already exists","flawless_userid":str(a.key())}
			return resp
		else:
			u = cls(email = email,password = password, date_of_birth = dob,phone=phone,first_name=first_name,last_name=last_name)

			if data.has_key('facebook_id'):
				u.facebook_id = data['facebook_id']
			
			if data.has_key('twitter_id'):
				u.twitter_id = data['twitter_id']

			u.put()
			log.info(kwargs)
			log.info("created method is called =====================")
			resp = {"status":True,"message":"ok","flawless_userid":str(u.key())}
			return resp

	@classmethod
	def login(cls,request,data,**kwargs):
		email = data['username']
		password = data['password']
		u = User.gql("where email = :1",email)
		u = u.get()
			
		if u is None:
			resp = {"status":False,"message":"Email does not exist."}
			return resp
		else:
			if u.password == password:
				resp = {"status":True,"message":"success","flawless_userid":str(u.key())}
				""" update device token if users logs in from a different device """
				return resp
			else:
				resp = {"status":False,"message":"Invalid password"}
				return resp

	@classmethod
	def fblogin(cls,request,data,**kwargs):
		fbid = data['facebook_id']
		u = User.gql("where facebook_id = :1",fbid)
		u = u.get()
			
		if u is None:
			resp = {"status":False,"message":"Invalid FacebookId"}
			return resp
		else: 
			key = u.key()
			resp = {"status":True,"user_id":str(key)}
			return resp 

	@classmethod
	def tlogin(cls,request,data,**kwargs):
		tid = data['twitter_id']
		u = User.gql("where twitter_id = :1",tid)
		u = u.get()
			
		if u is None:
			resp = {"status":False}
			return resp
		else:
			resp = {"status":True}
			return resp  

	@classmethod
	def pwdreset(cls,request,data,**kwargs):
		newpwd = data['newpwd']
		oldpwd = data['oldpwd']
		email = data['username']
		q = db.GqlQuery("SELECT * from User where password = :1 and email =:2",oldpwd,email)
		a = q.get()
		if a is not None:
			a.password = newpwd
			a.put()
			resp = {"status":True,"message":"password changed successfully"}
			return resp
		else:
			resp = {"status":False,"message":"Please check your email and password"}
			return resp

	@classmethod
	def forgotpwd(cls,request,data,**kwargs):
		email = data['email']
		to_addr = email
		q = db.GqlQuery("SELECT * from User where email = :1",email)
		a = q.get()
		if a is None:
			resp = {"status":False,"message":"Email doesnot exist"}
			return resp
		else:
			user = a.key()
			message = mail.EmailMessage()
			message.sender = "manjurakurty@gmail.com"
			message.to = to_addr
			message.body = 'Password:%s'%a.password
			message.send()
			resp = {"status":True,"message":"success"}
			return resp
