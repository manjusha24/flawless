import webapp2
from webapp2_local.session import SessionHandler
from webapp2_extras import sessions
from webapp2_extras import mako


class SessionHandler(webapp2.RequestHandler):
	def dispatch(self):
		try:
			webapp2.RequestHandler.dispatch(self)
		finally:
			self.session_store.save_sessions(self.response)

	@webapp2.cached_property
	def session_store(self):
		return sessions.get_store(request=self.request)

	@webapp2.cached_property
	def session(self):
		return self.session_store.get_session() 


class BaseHandler(SessionHandler):
	def dispatch(self):
		super(BaseHandler,self).dispatch()

	@webapp2.cached_property
	def mako(self):
		# Returns a Mako renderer cached in the app registry.
		return mako.get_mako(app=self.app)

	def render_response(self, _template, **context):
		# Renders a template and writes the result to the response.
		rv = self.mako.render_template(_template, request=self.request, session=self.session, **context)
		self.response.write(rv) 
