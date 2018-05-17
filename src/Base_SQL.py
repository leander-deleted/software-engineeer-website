# -*- coding:utf8 -*-
'''

 
'''



import pymysql
import time
import json

# 获取系统时间 time.strftime('%Y-%m-%d-%H:%M',time.localtime(time.time()))

conn=pymysql.connect(host='localhost',
    user='root',
    passwd='277435',
    port=3306,
    charset = 'utf8',
    cursorclass = pymysql.cursors.DictCursor,
    db = "a1"
    )
cur=conn.cursor()





def Admin_Order_function():
    order_dict = {}
    data_dict = {}
    return_dict = {}
    sqlstr = "SELECT id, user_id, goods_name, goods_num, sum, deal_time, pay FROM order_table"
    count = cur.execute(sqlstr)
    result = cur.fetchall()
    for item in result:
        order_dict['uid'] = str(item[1])
        order_dict['name'] = str(item[2])
        order_dict['num'] = int(item[3])
        order_dict['sum']= int(item[4])
        order_dict['time'] = str(item[5])
        order_dict['statue'] = int(item[6])
        order_id = "%03d"%int(item[0])
        data_dict[order_id] = order_dict
        order_dict = {}
    return_dict['length'] = int(count)
    return_dict['data'] = data_dict
    print return_dict
    return return_dict


def Admin_Allusers_function():
    return_dict = {}
    data_dict = {}
    user_dict = {}
    sqlstr = "SELECT id, account, password, addr, tel FROM user_table  ORDER BY id"
    count = cur.execute(sqlstr)
    result = cur.fetchall()
    for item in result:
        user_id = "%03d"%int(item[0])
        user_dict['account'] = str(item[1])
        user_dict['addr'] = str(item[3])
        user_dict['tel'] = str(item[4])
        data_dict[user_id] = user_dict
        user_dict = {}
    return_dict['length'] = int(count)
    return_dict['data'] = data_dict
    print return_dict
    return return_dict


def Admin_AllGoods_function():
    return_dict = {}
    data_dict = {}
    good_dict = {}
    sqlstr = "SELECT id, name, kind, price, discount  FROM goods_table  ORDER BY id"
    count = cur.execute(sqlstr)
    result = cur.fetchall()
    for item in result:
        good_id = "%03d"%int(item[0])
        good_dict['name'] = str(item[1])
        good_dict['type'] = str(item[2])
        good_dict['price'] = int(item[3])
        good_dict['off'] = int(item[4])
        data_dict[good_id] = good_dict
        good_dict = {}
    return_dict['length'] = int(count)
    return_dict['data'] = data_dict
    print return_dict
    return return_dict

# 修改商品价格
def  Admin_Modify_Price_function(good_id, price):
    try:
        sqlstr = "UPDATE goods_table SET price = %s" %price
        cur.execute(sqlstr)
        conn.commit()
        print 'result : 1'
        return 1
    except:
        print 'result : 0'
        return 0


# 修改商品折扣
def Admin_Modify_Discount_function(good_id, re_discount):
    try:
        sqlstr = "UPDATE goods_table SET discount = %s" %re_discount
        cur.execute(sqlstr)
        conn.commit()
        print 'result : 1'
        return 1
    except:
        print 'result : 0'
        return 0


# 删除订单
def Admin_Del_Order_function(order_id):
    try:
        sqlstr = " DELETE FROM order_table WHERE id  = %s" %int(order_id)
        cur.execute(sqlstr)
        conn.commit()
        print 'result : 1'
        return 1
    except:
        print 'result : 0'
        return 0


# 删除用户
def Admin_Del_User_function(user_id):
    try:
        sqlstr = " DELETE FROM user_table WHERE id  = %s" %int(user_id)
        cur.execute(sqlstr)
        conn.commit()
        print 'result : 1'
        return 1
    except:
        print 'result : 0'
        return 0


# 根据id返回表中的detail字段 ,  如果不存在此id，返回0
def Detail_function(id):
    id = int(id)
    details = {}
    sqlstr = "SELECT name, detail, price, discount, kind FROM  goods_table WHERE id = %d" %id
    count = int(cur.execute(sqlstr))
    if count != 0:
        result = cur.fetchone()
        # print result
        details['name'] = str(result["name"])
        details['detail'] = str(result["detail"])
        details['price'] = int(result["price"])
        details['discount'] = int(result["discount"])
        details['tag'] = str(result["kind"])
    print details
    return details


def get_username(user_id):
    sql = "select account from user_table where id=%d" %int(user_id)
    cur.execute(sql)
    username = cur.fetchone()
    print(username)
    return username['account']




def Home_Userinfo_function(user_id):
    user_id = int(user_id)
    user_dict = {}
    sqlstr = "SELECT account, addr, tel FROM user_table  WHERE id = %d" %user_id
    cur.execute(sqlstr)
    user_info = cur.fetchone()
    user_dict['account'] = str(user_info["account"])
    user_dict['addr'] = str(user_info["addr"])
    user_dict['tel'] = str(user_info["tel"])
    return user_dict


def Home_Orderinfo_function(user_id):
    user_id = int(user_id)
    order_dict = {}
    data_arr = []
    return_dict = {}
    sqlstr = "SELECT id, user_id, good_id, goods_name, goods_num,  sum, deal_time, pay FROM order_table  WHERE user_id = %d" %user_id
    count = cur.execute(sqlstr)
    result = cur.fetchall()
    for item in result:
        # userid
        order_dict['uid'] = str(item["user_id"])
        # order id 
        order_dict['oid'] = item["id"]
        print("order_id",order_dict['oid'] )
        # goods name
        order_dict['name'] = str(item["goods_name"])
        # goods number
        order_dict['num'] = str(item["goods_num"])
        # goods sum
        order_dict['sum'] = int(item["sum"])
        # deal time
        order_dict['time'] = str(item["deal_time"])
        # status
        order_dict['statue'] = int(item["pay"])
        # userid
        data_arr.append(order_dict)
        order_dict = {}
    return_dict['length'] = int(count)
    return_dict['data'] = data_arr
    print return_dict
    return return_dict



# 登录成功返回用户id，失败返回0
# acc: username ; passwd: password
def Login_function(acc, passwd):
    result ={}
    sqlstr = "SELECT id FROM user_table WHERE account = '%s' AND password = '%s'" %(acc, passwd)
    count = int(cur.execute(sqlstr))
    if count == 0:
        user_id = 0
        result = {'flag':False,"user_id":user_id}
    else:
        user_id = cur.fetchall()[0]["id"]
        result = {'flag':True,"user_id":user_id}
    print("result in Login_function:",result)
    return result 



# 查询功能，根据商品类别查出所有商品，并返回   注：没有考虑查不到的情况, length = 0
def List_function(ttype):
    goods_dict = {}
    return_dict = {}
    sqlstr = "SELECT id,name, price,discount FROM goods_table WHERE kind = '%s'" %ttype
    count = cur.execute(sqlstr)
    if count == 0:
        return_dict['length'] = int(count)
        return_dict['data'] = {}
        # print return_dict
        return return_dict
    else:
        result = cur.fetchall()
        print("result is : ",result)
        for item in result:
            print("item is ",item)
            if item["discount"]:
                discount = int(item["discount"])
            else:
                discount = 1
            goods_id = "%03d"%int(item["id"])
            goods_dict[goods_id] = [str(item["name"]), int(item["price"]), discount]
            print ("goods_dict",goods_dict)
        return_dict['length'] = int(count)
        return_dict['data'] = goods_dict
        print ("return_dict is :",return_dict)
        return return_dict


def Main_list():
    goods_dict = {}
    return_dict = {}
    sqlstr = "SELECT id,name, price,discount FROM goods_table"
    count = cur.execute(sqlstr) #1-2
    result = cur.fetchall()
    for item in result:
        if item["discount"]:
            discount = int(item["discount"])
        else:
            discount = 1
        goods_id = "%03d"%int(item["id"])
        goods_dict[goods_id] = [str(item["name"]), int(item["price"]), discount]
    return_dict['length'] = int(count)
    return_dict['data'] = goods_dict
    print return_dict
    return return_dict



def Order_function(user_id):
    #  商品dict
    goods_dict = {} 
    # 每条订单dict
    order_dict = {} 
    # 最终返回的dict
    return_dict = {} 
    sqlstr = "SELECT id, sum,deal_time,good_id, goods_name, goods_num FROM order_table WHERE user_id = '%s' " %(user_id)
    count = cur.execute(sqlstr)
    result = cur.fetchall()
    if count == 0:
        pass
    else:
        for item in result:
            goods_dict[int(item["good_id"])]=[str(item["goods_name"]),int(item["goods_num"])]
            order_dict['sum'] = int(item[1])
            order_dict['time'] = str(item[2])
            order_dict['goods']  = goods_dict
            return_dict[int(item["id"])] = order_dict
            goods_dict = {}
            order_dict = {}
        print return_dict

def Order_del_function(order_id):
    try:
        sqlstr = "DELETE FROM order_table WHERE id = %s" %int(order_id)   
        cur.execute(sqlstr)
        conn.commit()
        print 'result : 1'
        return 1
    except:
        print 'result : 0'
        return 0

# generate order
def Purchase_function(good_id, num, user_id):
    try:
        sqlstr = "SELECT id,name, price,discount FROM goods_table WHERE id = '%s'" %str(good_id)
        cur.execute(sqlstr)
        result = cur.fetchone()
        print(result)
        price = int(result["price"])
        # print("price",price)
        #sum of money
        sum1 = price * num
        # print("sum1",sum1)
        now_time = time.strftime('%Y-%m-%d-%H:%M',time.localtime(time.time()))
        # print(now_time)
        sqlstr = "INSERT INTO order_table(user_id, good_id, goods_name, goods_num, sum, deal_time,pay) VALUES('%s', '%s', '%s', %d, %d, '%s','%d')" %(str(user_id), str(good_id), str(result["name"]), num, sum1, str(now_time),0)
        print(sqlstr)
        cur.execute(sqlstr)
        conn.commit()
        print "Order ok ..."
        return 1
    except:
        print("error")
        return 0



# 确认支付
def Purchase_commit_function(order_id):
    try:
        sqlstr = "UPDATE order_table SET pay = 1 WHERE id = %d " %int(order_id) 
        print(sqlstr)  
        cur.execute(sqlstr)
        conn.commit()
        print 'result : 1'
        return 1
    except:
        print 'result : 0'
        return 0


def Reg_function(account, passwd, addr ,tel):
    # account: all existing account
    accounts = []
    sqlstr = "SELECT account FROM user_table"
    cur.execute(sqlstr)
    # fetchall return a list, element is dictrionary
    result = cur.fetchall() #1-1
    print(result)
    for item in result:
        accounts.append(str(item["account"]))
    if account in accounts:
        user_id = 0
    else:
        sqlstr = "INSERT INTO user_table(account, password, addr, tel) VALUES('%s','%s','%s','%s') " %(account, passwd, addr,tel)
        cur.execute(sqlstr)
        conn.commit()
        sqlstr = "SELECT id FROM user_table WHERE account = '%s' AND password = '%s'" %(account, passwd)
        cur.execute(sqlstr)
        # result: selection of registration user
        result = cur.fetchone()
        user_id = int(result["id"])

    assert type(user_id) == int 
    return user_id


# 查询功能，根据商品名称查出所有商品，并返回    注：没有考虑查不到的情况 length = 0
def Search_function(item):
    goods_dict = {}
    return_dict = {}
    sqlstr = "SELECT id,name, price,discount FROM goods_table WHERE name like '%{}%'".format(item)
    count = cur.execute(sqlstr)
    if count == 0:
        return_dict['length'] = int(count)
        print return_dict
        return return_dict
    else:
        result = cur.fetchall()
        for item in result:
            if item["discount"]:
                discount = int(item["discount"])
            else:
                discount = 1
            goods_id = "%03d"%int(item["id"])
            goods_dict[goods_id] = [str(item["name"]), int(item["price"]), discount]
        return_dict['length'] = int(count)
        return_dict['data'] = goods_dict
        print return_dict
        return return_dict



if __name__ == '__main__':
    # Main_list()
   #  Login_function('123', 'abc123')
   # List_function('A')
    # Detail_functioni('001')
    # Reg_function('795', 'abc123', 'HIT' ,'18963166073')
   #  Search_function('computer')
  #  Order_function('002')
  # Admin_Order_function()
 # Admin_Allusers_function()
 # Admin_Modify_Price_function(1, 50)
 # Admin_Modify_Discount_function(2, 9)
 # Admin_Del_Order_function('003')
 # Admin_Del_User_function('013')
 # Purchase_Ctrl_function('001')
 # Admin_AllGoods_function()
 # Home_function('012')
 # Home_Orderinfo_function(2)
    Purchase_function("3",3,"123")
