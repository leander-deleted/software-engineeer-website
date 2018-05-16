/*

jquery#1
    $(document).ready()  #1-1
    $().html() #1-2
    $(this)
    $.cookie() 1-4
    find() 1-5
    val() 1-6
    text()1-7
    attr() 1-8
    $.post() 1-9
    $.ajax()1-10

location.href 2

array 3
    push
*/

$(document).ready(function () { //#1-1
    //'cartlen': the name of cookie; set value of cookies: $.cookie('cartlen',1)
    var cartlen = $.cookie('cartlen'); //1-4
    if (cartlen == 0) {
        cart = [];
    }
    else {
        cart = ana_ids($.cookie('cart'));
        var st = ''
        // console.log(cart)
        for (var i in cart) {
            st = st + '<tr alt="' + cart[i]['id'] + '"><td colspan="1" class="goods text-center"><label>' + cart[i]['name'] + '</label></td><td colspan="2" class="ext-center"><img src="static/images/goods/' + cart[i]['id'] + '.jpg" height="50" width="50"/></td><td class="selling-price number small-bold-red text-right"style="padding-top: 1.1rem;" data-bind="' + cart[i]['price'] + '">' + cart[i]['price'] + '</td><td><div class="input-group input-group-sm"> <span class="input-group-addon minus">-</span> <input type="text" class="number form-control input-sm" value="' + cart[i]['num'] + '" /><span class="input-group-addon plus">+</span></div></td><td class="subtotal number small-bold-red text-right" style="padding-top: 1.1rem;"></td><td class="action" style="padding-top: 1.1rem;"><span class="delete btn btn-xs btn-warning">删除</span></td></tr>'
        }
        $('#cartTable tbody').html(st) //#1-2

    }



    function getSubTotal(row) {
        var price = parseFloat($(row).find(".selling-price").data("bind"));
        //find(): find descendent node by filter
        //val(): return the value of value attribute; val(value): set the value of value attribute
        var qty = parseInt($(row).find(":text").val()); //1-5, 1-6
        var result = price * qty;
        // text(): return the text element of node, text(value):set text to element
        $(row).find(".selling-price").text($.formatMoney(price, 2)); //1-7
        // data() store key-value data at element
        $(row).find(".subtotal").text($.formatMoney(result, 2)).data("bind", result.toFixed(2)); //1-8
    };

    /*
     * 计算购物车中产品的累计金额
     */
    function getTotal() {
        var qtyTotal = 0;
        var itemCount = 0;
        var priceTotal = 0;
        $(cartTable).find("tr:gt(0)").each(function () {
            getSubTotal(this);
                itemCount++;
                qtyTotal += parseInt($(this).find(":text").val());
                priceTotal += parseFloat($(this).find(".subtotal").data("bind"));
            
        });
        $("#itemCount").text(itemCount).data("bind", itemCount);
        $("#qtyCount").text(qtyTotal).data("bind", qtyTotal);
        $("#priceTotal").text($.formatMoney(priceTotal, 2)).data("bind", priceTotal.toFixed(2));
    };

    var cartTable = $("#cartTable");

    getTotal();

 
    $(cartTable).find("tr:gt(0)").each(function () {
        var input = $(this).find(":text");
        // attr(): get value of specified attribute
        var id = $(this).attr('alt'); //1-8

        //为数量输入框添加事件，计算金额小计，并更新总计
        //keyup: the event; function: handler to event
        $(input).keyup(function () { //1-9
            var val = parseInt($(this).val());
            if (isNaN(val) || (val < 1)) { $(this).val("1"); }
            getSubTotal($(this).parent().parent()); //tr element
            getTotal();
        });

        //为数量调整按钮、删除添加单击事件，计算金额小计，并更新总计
        $(this).click(function () {
            var val = parseInt($(input).val());
            if (isNaN(val) || (val < 1)) { val = 1; }

            if ($(window.event.srcElement).hasClass("minus")) {
                if (val > 1) {
                    val--;
                    input.val(val);
                    getSubTotal(this);
                    minus(id);
                }
            }
            else if ($(window.event.srcElement).hasClass("plus")) {
                if (val < 9999) val++;
                input.val(val);
                getSubTotal(this);
                add(id);
            }
            else if ($(window.event.srcElement).hasClass("delete")) {
                if (confirm("确定要从购物车中删除此产品？")) {
                    $(this).remove();
                    del(id);
                }
            }
            getTotal();
        });
    });
});

function gen_order() {
    var cart = [];
    cart = ana_ids($.cookie('cart'));
    dict = []
    //item: goods item
    console.log("cart",cart)

    // for (var i in cart) {
    //     // push a element at the back of array
    //     //id: goods id
    //     console.log("item:",cart[i])
    //     dict[i] = [cart[i]['id'],cart[i]['num']]

    //     dict.push(cart[i]); //3
    // };
    //dict: send argument with post request, eg: $.post( "test.php", { name: "John", time: "2pm" } );
    // console.log("dict:",dict)

    $.ajax({ //1-10
        type:'post',
        url:'/purchase',
        data:{cart},
    })
    .done(function (data) { //1-9
        if(data=="true"){
        alert('购买成功！')
        $.cookie('cartlen', 0);
        $.cookie('cart', '');
        // redirect to new url
        location.href = '/profile'; //2
    }
        else{
            alert("购买失败");
        }
    })

};