from bs4 import BeautifulSoup
import mechanize
from urllib2 import urlopen
import getpass
import cookielib

class TwitterNotif:
	def __init__(self, user, password):
		self.br = mechanize.Browser()
		self.cookie = cookielib.LWPCookieJar()
		self.br.set_cookiejar(self.cookie)	
		self.br.set_handle_robots(False)
		self.user = user 
		self.password = password
		
	def login(self):
		self.br.open('https://mobile.twitter.com')
		self.br.select_form(nr=0)
		self.br.form['session[username_or_email]'] = self.user
		self.br.form['session[password]'] = self.password
		self.br.submit()

	def get_notifications(self):
		notifPage = BeautifulSoup(self.br.open('https://mobile.twitter.com/i/connect').read())
		timeline = notifPage.find('div', class_="timeline")
		timeline = timeline.findAll('table')
		text_tweet = []
		date_tweet = []
		user_tweet = []
		for each in timeline:
			tweet = each.findAll('div', class_="dir-ltr")
			date = each.findAll('td', class_="timestamp")
			if len(each['class']) == 1: #Activity
				username = each.findAll('div', class_="user")
				if len(tweet) == 0:
					text_tweet.append('')				
			elif len(each['class']) == 2: #Tweet
				username = each.findAll('span', class_="username")
				#Get the date of each tweet
			for d in date:
				date_tweet.append((d.get_text()).replace('\n',''))
			#Get the username of each tweet
			for u in username:
				user_tweet.append((u.get_text()).replace('\n',''))
			#Get the text of each tweet			
			for t in tweet: 
				text_tweet.append(t.get_text())
			
		for u,d,t in zip(user_tweet, date_tweet, text_tweet):
			print "From: "+u+"  "+d
			print "  "+t
			print

      
username = raw_input("Enter username, telephone or email: ")
log = getpass.getpass("Password: ")
print
print(" _   _       _   _  __ _           _   _ \n"                
	  "| \ | | ___ | |_(_)/ _(_) ___ __ _| |_(_) ___  _ __  ___ \n"
	  "|  \| |/ _ \| __| | |_| |/ __/ _` | __| |/ _ \| '_ \/ __|\n"
	  "| |\  | (_) | |_| |  _| | (_| (_| | |_| | (_) | | | \__ \\\n"
	  "|_| \_|\___/ \__|_|_| |_|\___\__,_|\__|_|\___/|_| |_|___/\n")

try:
	t = TwitterNotif(username, log)
	t.login()
	t.get_notifications()
except:
	print("Uppss! Something went wrong...Please, try it again")
