$(document).ready(function(){
	var form=$("#buy-form");


	function busketUpdating(product_id,nmb,is_delete,href=''){
	 	var data={};
	 	data.product_id = product_id;
	 	data.nmb = nmb;
	 	var csrf_token = $('[name="csrfmiddlewaretoken"]').val();
	 	data["csrfmiddlewaretoken"] = csrf_token;

	 	if (is_delete){
	 		data["is_delete"] = true;
	 	}
	 	console.log(data);
	 	var url = form.attr("action");
	 	if (url){

	 	}
	 	else{
	 		url = href;
	 	}
	 	$.ajax({
	 		url: url,
	 		type: 'POST',
	 		data: data,
	 		cache: true,
	 		success: function (data) {
	 			console.log("OK");
	 			console.log(data.products_total_nmb);
	 			$('#total-count').text(data.products_total_nmb);
	 			// if (data.products_total_nmb || data.products_total_nmb == 0){
	 			// 	$('#count_in_basket').text(data.products_total_nmb);
	 			// 	$('#count_in_basket_small').text(data.products_total_nmb);
	 			// 	// $('#basket_total_nmb').text("("+data.products_total_nmb+")");
	 			// 	// console.log(data.products);
	 			// 	$('#basket_items tbody').html("");
	 			// 	$.each(data.products, function(k, v){
	 			// 		console.log('im here');
	 					
	 			// 	});
	 			// }
	 		},
	 		error: function(){
	 			console.log("error")
	 		}
	 	})
	}
	$(document).on('click','.bt9',function(event){
		event.preventDefault();
		var form=$(event.target).closest('#buy-form');
		if (form){
			var product=form.find('#buy-btn');
			// var input=form.find('.counter_block');
			// var in_basket=form.find('#in-basket-btn');
			console.log(product);
			var id=product.data('id');
			var nmb=form.find('#bx_quantity').val();
			console.log(id);
			console.log(nmb);
			busketUpdating(id,nmb,is_delete=false);
			// product.hide();
			// input.hide();
			// in_basket.show();

		}
		else{
			return;
		}
	});
	$(document).on('click','.buy-btn',function(event){
		console.log('f');
		event.preventDefault();

		var form=$(event.target).closest('#buy-form');
		console.log(form);
		if (form){
			var product=form.find('.buyLinks');
			// var input=form.find('.counter_block');
			// var in_basket=form.find('#in-basket-btn');
			var id=product.data('id')
			busketUpdating(id,1,is_delete=false);
			// product.hide();
			// input.hide();
			// in_basket.show();

		}
		else{
			return;
		}
	})
	$(document).on('click','.deleteitem',function(event){
		event.preventDefault();
		var item=$(event.target).closest('.deleteitem');
		var url = item.attr('href');
		var id = item.data('id');
		console.log(url);
		busketUpdating(id,1,is_delete=true,href=url);
		var row = item.closest('.basket-row');
		row.remove();

	})
});
	