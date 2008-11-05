import urllib
import urllib2

theurl = '192.168.1.1'
protocol = 'http://'
username = 'admin'
password = 'admin'
# a great password

passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
# this creates a password manager
passman.add_password(None, theurl, username, password)
# because we have put None at the start it will always
# use this username/password combination for  urls
# for which `theurl` is a super-url

authhandler = urllib2.HTTPBasicAuthHandler(passman)
# create the AuthHandler

opener = urllib2.build_opener(authhandler)

urllib2.install_opener(opener)
# All calls to urllib2.urlopen will now use our handler
# Make sure not to include the protocol in with the URL, or
# HTTPPasswordMgrWithDefaultRealm will be very confused.
# You must (of course) use it when fetching the page though.

pagehandle = urllib2.urlopen(protocol + theurl)
# authentication is now handled automatically for us

url = "http://192.168.1.1/userRpm/StatusRpm.htm"
print url
pagehandle = urllib2.urlopen(url)
html=pagehandle.read()
wanPara_left_index = html.index("var wanPara = new Array")
#print wanPara_left_index
wanPara_right_index = html.rindex("var wlanPara = new Array(")
#print wanPara_right_index
wanPara = html[wanPara_left_index:wanPara_right_index]
wanPara = wanPara.replace('var wanPara = new Array(', '')
wanPara = wanPara.replace(');', '')
#print wanPara
wanParaList = wanPara.split(', ')
wanIp = wanParaList[2]
wanIp = wanIp.replace('"', '')
print wanIp

url = 'http://localhost:8080/sign'
values = {'hostname' : 'jinzy.biviz.com',
          'ip' : wanIp}

data = urllib.urlencode(values)
req = urllib2.Request(url, data)
response = urllib2.urlopen(req)
the_page = response.read()

