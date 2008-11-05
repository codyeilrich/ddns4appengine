import cgi
import os

from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class DNSARecord(db.Model):
  hostname = db.StringProperty()
  ip = db.StringProperty()

class MainPage(webapp.RequestHandler):
  def get(self):
    dnsarecord_query = DNSARecord.all().order('hostname')
    dnsarecords = dnsarecord_query.fetch(10)

    if users.get_current_user():
      url = users.create_logout_url(self.request.uri)
      url_linktext = 'Logout'
    else:
      url = users.create_login_url(self.request.uri)
      url_linktext = 'Login'

    template_values = {
      'dnsarecords': dnsarecords,
      'url': url,
      'url_linktext': url_linktext,
      }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

class Guestbook(webapp.RequestHandler):
  def post(self):
    dnsarecord = DNSARecord()

    #if users.get_current_user():
    #  greeting.author = users.get_current_user()

    dnsarecord.hostname = self.request.get('hostname')
    dnsarecord.ip = self.request.get('ip')
    dnsarecord.put()
    self.redirect('/')

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', Guestbook)],
                                     debug=True)

def main():
  run_wsgi_app(application)

if __name__ == "__main__":
  main()