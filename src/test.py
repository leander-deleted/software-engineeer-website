# -*- coding:utf8 -*-
# this must be put in the first line
'''
py2: #2

encode #2-1




tornado:#1

tornado.web.RequestHandler#1-1
	post() #1-1-1
	get() #1-1-2
	write() #1-1-3
	get_argument() #1-1-4

tornado.web.Application() #1-2

tornado.options #1-3
	parse_commandline() #1-3-1
	define() #1-3-2
	port 

tornado.httpserver #1-4
	httpserver.HTTPServer() #1-4-1
	httpserver.listen()  #1-4-2

tornado.ioloop.IOLoop#1-5
	instance() #1-5-1
	start() #1-5-2

os.path#2
	join() #2-1
	dirname() #2-2

__file__ #3

'''




import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import random
# import MySQLdb


from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int) #1-3-2


class MainHandler(tornado.web.RequestHandler):#1-1
    def post(self): #1-1-1

        pass

    def get(self): #1-1-2
        # self.render('xixi.html', state="")
        phone = self.get_argument('type') #1-1-4
        self.write(phone) #1-1-3
        # phone = self.get_argument('type')
        # print phone
        #self.write(self.request.headers['user-agent'] +\
			#"\nyour current ip is: "+self.request.remote_ip)

        #posturl="index.html"
        # self.render("")


class SearchHandler(tornado.web.RequestHandler):
    #更换种子
    def post(self):
        user = self.get_argument('user')
        sqlstr = "SELECT password FROM user WHERE user='%s'" % user
        cur.execute(sqlstr)
        password = cur.fetchone()[0]
        seed = random.randint(1,0xFFFFFFFF-1)
        last = hashlib.md5(str(password | seed)).hexdigest()
        #last = str((int(last)/0xFFFF)^(int(last)%0xFFFF))
        for i in range(0,10):
            last = hashlib.md5(last).hexdigest()
        #last = hashlib.md5((last_t/0xFFFF)^(last_t%0xFFFF))
        sqlstr = "UPDATE user SET seed = %d, lastkey = '%s' WHERE user='%s'" % (seed, last, user)
        cur.execute(sqlstr)
        conn.commit()
        self.write(str(seed))
        with open('Log.txt','a+') as f:
            f.write('Change Seed:%s\n'%user)
            f.close()

def test():
	tornado.options.parse_command_line() #1-3-1
	app = tornado.web.Application(handlers=[(r"/xixi.html", MainHandler),],
									static_path=os.path.join(os.path.dirname(__file__), "static"), #2-1 #2-2 #3
									template_path=os.path.join(os.path.dirname(__file__), "template"),
									debug=True) #1-2

	http_server = tornado.httpserver.HTTPServer(app) #1-4-1
	http_server.listen(options.port) #1-4-2
	tornado.ioloop.IOLoop.instance().start() # 1-5-1 #1-5-2


if __name__ == "__main__":
	print(__file__)
