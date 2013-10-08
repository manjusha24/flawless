from formencode import validators,national
import logging as log
from webapp2_extras import json
from datetime import datetime

def validationerrors(self,items):
	errors = []
	for f in items:
		field = f[0]
		field_type = f[1]
		data = json.decode(self.body)
		value = data[field]
        
		"""if field_type == "date":
			try:
				dob = validators.DateConverter(month_style = 'yyyy-mm-dd').to_python(value)
			except Exception as e:
				errors.append("DOB should be in dd/mm/yyyy format")"""

		if field_type == "dateofbirth":
			try:
				dob = validators.DateConverter(month_style = 'dd/mm/yyyy').to_python(value)
				time = validators.TimeConverter(use_datetime = True).to_python("0:0")
				dob = datetime.combine(dob,time)
				"""try:
					validators.DateValidator(earliest_date = datetime(1988,1,1)).to_python(dob)
				except Exception as e:
					errors.append("DOB should be after 01/01/1988")"""
			except Exception as e:
				errors.append("DOB should be in dd/mm/yyyy format")

					#email field
		elif field_type == "email":
			try:
				validators.Email(not_empty=True).to_python(value)
			except Exception as e:
				errors.append("Invalid email.")

					#password field
		elif field_type == "password":
			try:
				validators.String(not_empty=True).to_python(value)
			except Exception as e:
				errors.append("%s cannot be empty. "% field.capitalize())
				log.info(e)
					#string field 
		elif field_type == "phone":
			try:
				national.USPhoneNumber().to_python(value)
			except Exception as e:
				errors.append("Invalid phone number")
				log.info(e)

		elif field_type == 'string':
			try:
				validators.String(not_empty=True).to_python(value)
			except Exception as e:
				errors.append("%s cannot be empty. "% field.capitalize())
			else:
				try:
					validators.PlainText(Strip=True).to_python(value)
				except Exception as e:
					errors.append(e.msg)
		
		elif field_type == 'integer':
			try:
				validators.Int(not_empty=True).to_python(int(value))
			except Exception as e:
				errors.append("%s cannot be empty. "%field.capitalize())
				log.info(e)

		elif field_type == 'id':
			try:
				validators.NotEmpty(not_empty=True).to_python(value)
			except Exception as e:
				errors.append("%s cannot be empty. "% field.capitalize())

		elif field_type == 'statics':
			try:
				validators.NotEmpty(not_empty=True).to_python(value)
			except Exception as e:
				errors.append("%s cannot be empty. "% field.capitalize())

		elif field_type == 'notempty':
			try:
				validators.NotEmpty(not_empty=True).to_python(value)
			except Exception as e:
				errors.append("%s cannot be empty. "% field.capitalize()) 

	return errors


""" an awesome generic form validation decorator """

def validateForm(items):
	def decorator(func):
		def wrapper(self,*args,**kwargs):
			""" run the validation routine """
			errors = []
			request = self.request
			log.info("============================")
			log.info(type(request.body))
			log.info("============================")
			if request.method == 'POST':
				for f in items:
					field = f[0]
					field_type = f[1]
					try:
						data = json.decode(request.body)
						value = data[field]
						log.info(data)
						log.info("============================")
						log.info(value)
						log.info("============================")
					except Exception as e:
						errors.append("not a valid json format")
						return self.response.write(json.encode(errors))
				v = validationerrors(request,items)
				if len(v) > 0:
					e = ""
					for i in v:
						e += i+" " 
					resp = {"status":False,"message":e}
					return self.response.write(json.encode(resp))
				e = ""
				""" handle errors if any """
				if len(errors) > 0:
					for i in errors:
						e += i+"\n"
					er = {"error":True, "msg": e}
					self.response.content_type = "application/json" 
					return self.response.write(json.encode(er))
				else:
					return func(self,*args,**kwargs)
		return wrapper
	return decorator   


def apiMethod(callback):
	def decorator(func):
		def wrapper(self,*args,**kwargs):
			data = {}
			try:
				data = json.decode(self.request.body)
			except Exception as e:
				log.info(e)
			resp = callback(self.request,data,**kwargs)
 		 	self.response.content_type = "application/json" 
			return self.response.write(json.encode(resp)) 
		return wrapper
	return decorator
