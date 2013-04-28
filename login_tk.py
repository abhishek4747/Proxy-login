from getpass import getpass
from datetime import datetime
import urllib2,urllib,sys,threading,webbrowser

class Proxy:
    proxy_set={'btech':22,'dual':62,'diit':21,'faculty':82,'integrated':21,'mtech':62,'phd':61,'retfaculty':82,'staff':21,'irdstaff':21,'mba':21,'mdes':21,'msc':21,'msr':21,'pgdip':21}
	google = 'http://www.google.com'
	def __init__(self, username, password, proxy_cat):
		self.username = username
		self.password = password
		self.proxy_cat = proxy_cat
		self.auto_proxy = "http://www.cc.iitd.ernet.in/cgi-bin/proxy."+proxy_cat
		self.urlopener = urllib2.build_opener(urllib2.ProxyHandler({'auto_proxy':self.auto_proxy}))
		self.proxy_page_address = 'https://proxy'+str(Proxy.proxy_set[proxy_cat])+'.iitd.ernet.in/cgi-bin/proxy.cgi'
		self.new_session_id()
		

	def is_connected(self):
		proxies = {'http': 'http://proxy'+str(Proxy.proxy_set[self.proxy_cat])+'.iitd.ernet.in:3128'}
		try:
			response = urllib.urlopen(Proxy.google, proxies=proxies).read()
		except Exception, e:
			return "Not Connected"
		if "<title>IIT Delhi Proxy Login</title>" in response:
			return "Login Page"
		elif "<title>Google</title>" in response:
			return "Google"
		else:
			return "Not Connected"

	def get_session_id(self):
		try:
			response = self.open_page(self.proxy_page_address)
		except Exception, e:
			print "hello"
			return None
		check_token='sessionid" type="hidden" value="'
		token_index=response.index(check_token) + len(check_token)
		sessionid=""
		for i in range(16):
		    sessionid+=response[token_index+i]
		return sessionid

	def new_session_id(self):
		self.sessionid = self.get_session_id()
		self.loginform={'sessionid':self.sessionid, 'action':'Validate', 'userid':self.username, 'pass':self.password}
		self.logout_form={'sessionid':self.sessionid, 'action':'logout', 'logout':'Log out'}
		self.loggedin_form={'sessionid':self.sessionid, 'action':'Refresh'}

	def login(self):
		response = self.submitform(self.loginform)
		if "Either your userid and/or password does'not match." in response:
			return "Incorrect", response
		elif "You are logged in successfully as "+self.username in response:
			return "Success", response
		elif "already logged in" in response:
			return "Already", response
		elif "Session Expired" in response:
			return "Expired", response
		else:
			return "Not Connected", response

	def logout(self):
		response = self.submitform(self.logout_form)
		if "you have logged out from the IIT Delhi Proxy Service" in response:
			return "Success", response
		elif "Session Expired" in response:
			return "Expired", response
		else:
			return "Failed", response
	    
	def refresh(self):
		response = self.submitform(self.loggedin_form)
		if "You are logged in successfully" in response:
			if "You are logged in successfully as "+self.username in response:
				return "Success", response
			else:
				return "Not Logged In"
		elif "Session Expired" in response:
			return "Expired", response
		else:
			return "Not Connected", response

	def details(self):
		for property, value in vars(self).iteritems():
			print property, ": ", value

	def submitform(self, form):
		return self.urlopener.open(urllib2.Request(self.proxy_page_address,urllib.urlencode(form))).read()

	def open_page(self, address):
		return self.urlopener.open(address).read()

from Tkinter import *

class Proxy_login:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()

        self.top_label = Label(frame, text="Proxy Login")
        self.top_label.pack(side=TOP)

        self.btech = Button(frame, text="B.Tech", command=self.check_btech)
        self.btech.pack(side=LEFT)

        self.dual = Button(frame, text="Dual", command=self.check_dual)
        self.dual.pack(side=LEFT)

        self.mtech = Button(frame, text="Mtech", command=self.check_mtech)
        self.mtech.pack(side=LEFT)

        self.phd = Button(frame, text="Phd", command=self.check_phd)
        self.phd.pack(side=LEFT)

    def check_btech(self):
        print "Btech check"

    def check_mtech(self):
        print "Mtech check"

    def check_phd(self):
        print "Phd check"

    def check_dual(self):
    	print "Dual check"
    	if user1.is_connected()=='Login Page' or user1.refresh()=='Not Logged In':
    		user1.new_session_id()
    		log = user1.login()[0]
    		print "Login",log,datetime.now()
    		def ref():
    			res = user1.refresh()
    			if res=='Success':
    				self.top_label.config(text=user1.username)
    				threading.Timer(100.0,ref).start()
    			elif res=='Session Expired':
    				threading.Timer(10.0,self.check_dual).start()
    			else:
    				threading.Timer(10.0,self.ref).start()
    			print "Refresh",res,datetime.now()
    		threading.Timer(60.0,ref).start()
    	elif user1.refresh()[0]=='Success':
    		log = user1.logout()[0]
    		print "Logout",log,datetime.now()
    	else:
    		pass
    	set_window()


root = Tk()
app = Proxy_login(root)
# def doSomething():
# 	root.destroy()
# 	exit(0)
# root.protocol('WM_DELETE_WINDOW', doSomething)
def create():
	root.mainloop()


Dual = Proxy(username='', password='', proxy_cat='dual')
Btech = Proxy(username='', password='', proxy_cat='btech')
Mtech = Proxy(username='', password='', proxy_cat='mtech')
Phd = Proxy(username='', password='', proxy_cat='phd')
user1 = Proxy(username='username', password='password', proxy_cat='dual')

def set_window():
	dlog = Dual.is_connected()
	blog = Btech.is_connected()
	if (blog=='Google'):
		app.btech.config(fg='green')
	else:
		app.btech.config(fg='black')

	if (dlog=='Google'):
		if (user1.refresh()=='Success'): 
			app.dual.config(text='Logout')
			# app.top_label.config(text=user1.username)
		else: 
			app.dual.config(text='Dual')
			# app.top_label.config(text='Proxy Login')
		app.dual.config(fg='green')
	elif dlog=='Not Connected':
		pass
		# app.top_label.config(text='Not Connected')
	else:
		# app.top_label.config(text='Proxy Login')
		app.dual.config(fg='black')

def refresh_window():
	print 'rf_win',threading.active_count()
	set_window()
	threading.Timer(5.0,refresh_window).start()

threading.Timer(0,create).start()
refresh_window()

def read_user():
	ins = open( "file.txt", "r" )
	for line in ins:
		print line
# user2 = Proxy(username='username', password='password', proxy_cat='dual')
