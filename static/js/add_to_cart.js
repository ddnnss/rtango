function add_to_cart(el,num) {
    let item_number = 0
    if (num){
         item_number = num
    }
    else{
        item_number = document.getElementById('item_number').value
    }

    let item_id = el.dataset.item_id
    let item_name = el.dataset.item_name
    let item_price = el.dataset.item_price
    let item_image = el.dataset.item_image


    let csrfmiddlewaretoken = document.getElementsByName('csrfmiddlewaretoken')[0].value
    // console.log($(form).attr('action'));
    //  console.log(csrf_token);
        let data = {};
        data.item_id = item_id;
        data.item_number = item_number;
        data['csrfmiddlewaretoken'] = csrfmiddlewaretoken;

        console.log(data);
        $.ajax({
            url:'/cart/add_to_cart/',
            type:'POST',
            data: data,
            cache:true,
            success: function (data) {
                console.log('OK');
                console.log(data.total_items_in_cart);
                console.log(data.all_items);

                $('.cart_table_lg').empty();

                $.each(data.all_items,function (k,v) {
                    $('.cart_table_lg').append(
                         `   <li class="single-shopping-cart">
                                        <div class="shopping-cart-img">
                                            <a href="javascript: void(0)"><img width="50" height="50" alt="" src="${v.image}"></a>
                                        </div>
                                        <div class="shopping-cart-title">
                                            <h4><a href="javascript: void(0)">${ v.name}</a></h4>
                                            <h6>Количество ${v.number}</h6>
                                            <span>${v.total_price} &#8381;</span>
                                        </div>
                                        <div class="shopping-cart-delete">
                                            <a href="javascript: void(0)" data-item_id="${v.id}" onclick="delete_from_cart(this);return false;"><i class="ion ion-close"></i></a>
                                        </div>
                                    </li>`
                    );


                });


                $('.cart_total_lg').html(data.total_items_in_cart);
                $('.cart-total-cost').html(data.total_cart_price + ' &#8381;');
                $('.cart_footer_lg').html('');
                $('.cart_footer_lg').html(`<div class="shopping-cart-total ">                                 
                                    <h4>Всего : <span class="shop-total">${data.total_cart_price} &#8381;</span></h4>
                                </div>
                                <div class="shopping-cart-btn">
                                    <a href="/cart/">Корзина</a>
                                    <a href="checkout.html">Оплатить</a></div>`);

                 $('#cart_content_table').empty();


                $.each(data.all_items,function (k,v) {
                    $('#cart_content_table').append(`
                                        <tr>
                                            <td class="product-thumbnail">
                                                <a href="#"><img width="70px" src="${v.image}" alt=""></a>
                                            </td>
                                            <td class="product-name"><a href="#">${v.name}</a></td>
                                            <td class="product-price-cart"><span class="amount">${v.price} &#8381;</span></td>
                                            <td class="product-quantity">
                                                <div class="pro-dec-cart">
                                                    <input class="cart-plus-minus-box"  data-item_in_cart_id="${v.cart_id}" onchange="change_cart(this);return false;" type="number" min="1" value="${v.number}"  name="qtybutton">
                                                </div>
                                            </td>
                                            <td class="product-subtotal">${v.total_price} &#8381;</td>
                                            <td class="product-remove">

                                                <a onclick="delete_from_main_cart(${v.cart_id});return false;" title="Удалить">
                                                    <i class="fa fa-times"></i></a>
                                           </td>
                                        </tr>`

                    );
                });
                 $('#cart_total').html(data.total_cart_price);
                $('#cart_subtotal_price_side').html(data.total_cart_price + ' &#8381;');
                $('#cart_total_price_side').html(data.total_cart_price_with_discount + ' &#8381;');
                $('#promo_value').html(data.promo_discount_value + ' %');
                 getShippingPrice()


                $.amaran({
                        'theme'     :'user blue',
                        'content'   :{
                            img: item_image,
                            user:'Добавлено в корзину:',
                            message: item_number + ' шт. - ' + item_name
                        },
                        'position'  :'bottom right',
                        'outEffect' :'slideBottom'
                    });
            },
            error: function () {
                console.log('ERROR')
            }
        })
    }