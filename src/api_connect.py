# -*- coding:utf8 -*-


'''
(r"/", MainHandler),
(r"/off",OffHandler),
(r"/reg", RegHandler),
(r"/detail", DetailHandler),
(r"/login", LoginHandler),
(r"/cart", CartHandler),
(r"/home", HomeHandler),
(r"/list",ListHandler),
(r"/admin", AdminHandler),

sitemap:

# home.html
/  
# list.html
/list 
# login.html
/login



'''

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
import random
import Base_SQL
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)



class AdminHandler(tornado.web.RequestHandler):
    def post(self):
        type=self.get_argument('type')
        id=self.get_argument('id')
        # 这个id在相应情况下是用户号和订单号
        if type=='deluser':
            Base_SQL.Admin_Del_User_function(id)
        elif type=='delorder':
            # 删除订单;result为1,修改成功;为0,则修改失败,result为int
            Base_SQL.Admin_Del_Order_function(order_id)
        elif type=='changeprice':
            # 修改商品价格;result为1,修改成功;为0,则修改失败,result为int
            price=self.get_argument('price')
            result = Base_SQL.Admin_Modify_Price_function(id, price)
        elif type=='changeoff':
            # 修改商品折扣;result为1,修改成功;为0,则修改失败,result为int
            off=self.get_argument('off')
            result = Base_SQL.Admin_Modify_Discount_function(id, off)
    def get(self):
        #验证身份
        #判断请求类型
        try:
            type=self.get_argument('type')
            if type == 'order':
                # 管理员查看所有订单
                Orders = Base_SQL.Admin_Order_function()
                self.write(Orders)
            elif type == 'user':
                # 管理员查看所有用户
                All_users = Base_SQL.Admin_Allusers_function()
                self.write(All_users)
            elif type == 'goods':
                # 管理员查看所有商品
                All_goods = Base_SQL.Admin_AllGoods_function()
        except:
            self.render('admin.html')


class CartHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('cart.html')
    def post(self):
        #前端发送订单信息。需要验证是否登录
        #格式为{'商品id':数量}
        self.write('1')




# 根据id 查询商品详情，存在返回details，否则返回{}
class DetailHandler(tornado.web.RequestHandler):
    def get(self):
        user_id = self.get_cookie('cookie')
        username = Base_SQL.get_username(user_id)
        goods_id = self.get_argument('id')
        print("id is ",goods_id)
        details = Base_SQL.Detail_function(goods_id)
        if details != {}:
            price_now = int(details['price']*(100-details['discount'])/100)
            id = "%03d"%int(goods_id)
            self.render("product-detail.html",id=id,name=details['name'],price=details['price'],price_now=price_now,detail=details['detail'],tag=details['tag'],username=username)



class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        #验证身份
        user_id = self.get_cookie('cookie')
        user_dict = Base_SQL.Home_Userinfo_function(user_id)
        order_dict = Base_SQL.Home_Orderinfo_function(user_id)
        self.render('profile.html',account=user_dict['account'],addr=user_dict['addr'],tel=user_dict['tel'],length=order_dict['length'],data=order_dict['data'])
    def post(self):
        #不支持
        self.write('1')



class ListHandler(tornado.web.RequestHandler):
    def get(self):
        user_id = self.get_cookie('cookie')
        username = Base_SQL.get_username(user_id)
        ttype = self.get_argument('type')
        # print("type is ",ttype)
        goods_dict_return = Base_SQL.List_function(ttype)
        assert type (goods_dict_return) == dict
        self.render('list.html',length=goods_dict_return['length'], data=goods_dict_return['data'],username=username)



# 登录成功返回1,同时写cookie，登录失败返回0
class LoginHandler(tornado.web.RequestHandler):
    def post(self):
        account = self.get_argument('account')
        password = self.get_argument('password')
        result = Base_SQL.Login_function(account, password)
        print("result:",result)
        if result['flag'] == False:
            self.redirect('/login')
        else:
            # self.set_secure_cookie('user_id', result["user_id"])
            self.set_cookie("cookie",str(result["user_id"]))
            assert result['flag'] == True
            self.redirect('/')

    def get(self):
        self.render('login.html')


class LogoffHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("cookie")
        self.redirect('/')


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        user_id = self.get_cookie("cookie")
        if(not user_id):
            self.render('home.html',username="",flag=False)
        else:
            assert user_id != False
            username = Base_SQL.get_username(user_id)
            self.render('home.html',username=username,flag=True)



class OffHandler(tornado.web.RequestHandler):
    def get(self):
        goods_dict_return = Base_SQL.Main_list()
        self.write(goods_dict_return)


class OrderHandler(tornado.web.RequestHandler):
    def get(self):
         user_id = self.set_secure_cookie('user_id')
         order_dict_return = Base_SQL.Order_function(user_id)
         self.write(order_dict_return)


class PurchaseHandler(tornado.web.RequestHandler):
    def post(self):
         good_id = self.get_argument('good_id')
         good_num = self.get_argument('num')
         user_id = get_secure_cookie('user_id')
         Base_SQL.Purchase_function(good_id, num, user_id)



# 确认支付,根据uuid即order_id
class PurchaseCtrlHandler(tornado.web.RequestHandler):
    def post(self):
         order_id = self.get_argument('uuid')
         Base_SQL.Purchase_Ctrl_function(order_id)
                        
class RegisterHandler(tornado.web.RequestHandler):

    def post(self):
        account = self.get_argument('account')
        password = self.get_argument('password')
        addr = self.get_argument('addr')
        tel = self.get_argument('tel')
        print(type (account))
        assert type(account) == unicode 
        assert type(password) == unicode
        assert type(addr) == unicode
        assert type(tel) == unicode
        user_id = Base_SQL.Reg_function(account, password, addr, tel)
        if user_id == 0:
            self.redirect('/')

        else:
            self.set_cookie('cookie', str(user_id))
            self.redirect('/')

    def get(self):
        self.render('login.html')




class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        user_id = self.get_cookie('cookie')
        username = Base_SQL.get_username(user_id)
        item = self.get_argument('word')
        goods_dict_return = Base_SQL.Search_function(item)
        self.render("search-result.html",length = goods_dict_return['length'], data=goods_dict_return['data'],username=username )





if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", MainHandler),
                                            (r"/reg", RegisterHandler),
                                            (r"/detail", DetailHandler),
                                            (r"/login", LoginHandler),
                                            (r"/cart", CartHandler),
                                            (r"/home", HomeHandler),
                                            (r"/list",ListHandler),
                                            (r"/admin", AdminHandler),
                                            (r"/logoff",LogoffHandler),
                                            (r"/search",SearchHandler)
                                            ],
                                  static_path=os.path.join(os.path.dirname(__file__), "../static"),
                                  template_path=os.path.join(os.path.dirname(__file__), "../template"),
                                  debug=True,
                                  cookie_secret = "hello")

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    print("server is running. ")
    tornado.ioloop.IOLoop.instance().start()

