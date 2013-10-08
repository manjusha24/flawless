import webapp2
import webapp2_local
from views import home

route = [
  webapp2.Route(r'/', handler=home.Home, name='home'),
  webapp2.Route(r'/signup', handler=home.Signup, name='signup'),
  webapp2.Route(r'/login', handler=home.Login, name='login'),
  webapp2.Route(r'/fblogin', handler=home.FBLogin, name='fblogin'),
  webapp2.Route(r'/twlogin', handler=home.TLogin, name='twlogin'),
  webapp2.Route(r'/pwdreset', handler=home.Pwdreset, name='pwdreset'),
  webapp2.Route(r'/forgotpwd', handler=home.Forgotpwd, name='forgotpwd'),

]

config = {}
config['webapp2_extras.sessions'] = {
  'secret_key': 'eb27fb453030481832083ec9ad735cc7486cc675c5ad261544',
}

app = webapp2.WSGIApplication(route, config=config)
app.router.set_dispatcher(webapp2_local.custom_dispatcher)
