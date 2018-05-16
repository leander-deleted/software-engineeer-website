/*

parseInt() 1

string.substring() 2

object.length 3

*/

//id: goods_id
function add(id) {
    id = id.toString()
    if(id.length<3){
        if(id.length==2){
            id = '0'+id
        }
        else if(id.length ==1){
            id = "00"+id
        }
    }
    console.log("inside add function, id:",id)
    var cartlen = $.cookie('cartlen');
    var cart = [];
    if (cartlen == 0) {
        cart = [];
    }
    else {
        cart = ana_ids($.cookie('cart'));
    }
    var flag = 0;
    var i = 0
    for (i = 0; i < cart.length; i++) {
        if (cart[i]['id'] == id) {
            cart[i]['num']++;
            flag = 1;
        }
    }
    if (flag == 0) {
        cart[i] = { 'id': id, 'name': $('#name').text(), 'num': 1, 'price': $('[price]').attr('price') }
    }
    wrt_cart(cart);

};

function minus(id) {
    var cartlen = $.cookie('cartlen');
    var cart = [];
    if (cartlen == 0) {
        cart = [];
    }
    else {
        cart = ana_ids($.cookie('cart'));
    }
    var i = 0
    for (i = 0; i < cart.length; i++) {
        if (cart[i]['id'] == id) {
            cart[i]['num']--;
            if (cart[i]['num'] == 0) {
                cart.splice(i,1)
            }
        }
    }
    
    wrt_cart(cart);
};

function del(id) {
    var cartlen = $.cookie('cartlen');
    var cart = [];
    if (cartlen == 0) {
        cart = [];
    }
    else {
        cart = ana_ids($.cookie('cart'));
    }
    var i = 0
    for (i = 0; i < cart.length; i++) {
        if (cart[i]['id'] == id) {
            cart.splice(i, 1)
        }
    }

    wrt_cart(cart);

};

function GetQueryString(name) {
    var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)");
    var r = window.location.search.substr(1).match(reg);
    if (r != null) return decodeURI(r[2]); return null;
}

function search() {
    location.href = '/search?word=' + $('#search_txt').text();
}


// st: object of cookie('cart'), each item seperate by ; each term of item seperate by &
// ana_ids: return object of all choosed goods
function ana_ids(st) {
    cart = [];
    var goods_list_temp = [];
    if (typeof (st) != 'undefined') {
        goods_list_temp = st.split(';');
    }
    for (var i = 0; i < goods_list_temp.length; i++) {
        // a goods info
        info = goods_list_temp[i].split('&');
        //parseInt: parse string and return int value
        // id: goods_id; name: goods name; num: goods number; price: goods price
        cart[i] = { 'id': info[0], 'name': info[1], 'num': parseInt(info[2]), 'price': info[3] }; //1
    };
    return cart
};

// cart: object of cart
// wrt_cart: update cookis
function wrt_cart(cart) {
    var st = '';
    var i = 0;
    //length: count of attribute of object
    for (var i = 0; i < cart.length; i++) {//3
        st = st + cart[i]['id'] + '&' + cart[i]['name'] + '&' + cart[i]['num'] + '&' + cart[i]['price'] + ';';
    }
    //0: starting index, st.length-1: ending index
    st = st.substring(0, st.length - 1); //2
    $.cookie('cart', st);
    $.cookie('cartlen', i);
}

function ini() {
    // var account = $.cookie('account');
    var cartlen = $.cookie('cartlen');
    cart = $.cookie('cart');
    // if (account) {
    //     $('#user').html('<i class="fa fa-user"></i> ' + account);
    // }
    $('#cart').html('<i class="fa fa-heart-o"></i> 购物车 (' + cartlen + ') ');
}