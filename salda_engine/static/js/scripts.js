
 //Modal widnow controls
function CentriredModalWindow(ModalName){
	$(ModalName).css({"display":"block","opacity":0});
	var modalH = $(ModalName).height();
	var modalW = $(ModalName).width();
	$(ModalName).css({"margin-left":"-"+(parseInt(modalW)/2)+"px","margin-top":"-"+(parseInt(modalH)/2)+"px"})
}

function OpenModalWindow(ModalName){
	$(ModalName).animate({"opacity":1},300);	
	$("#bgmod").css("display","block");
}

function CloseModalWindow(){
	$("#bgmod").css("display","none");
	$(".modal").css({"opacity":1});
	$(".modal").animate({"opacity":0},300);
	setTimeout(function() { $(".modal").css({"display":"none"}); }, 500)	
}

$(".close").live('click', function() {
		CloseModalWindow()
	});

//Посчитаем количество элементов в слайдере и вычислим ширину Ul
$(document).ready(function(){
	if($(".a_cart #ant_bask_link").length == 0) $(".a_cart").hide();
    var li=$('.content.mp #foo_specialoffer li').length;
	var count=li*198;
	$('.content.mp #foo_specialoffer').css('width',count);
	
	var li=$('.content.mp #foo_recommend li').length;
	var count=li*198;
	$('.content.mp #foo_recommend').css('width',count);
	
	var li=$('.content.mp #foo_saleleader li').length;
	var count=li*198;
	$('.content.mp #foo_saleleader').css('width',count);
	
	var li=$('.content.mp #foo_newproduct li').length;
	var count=li*198;
	$('.content.mp #foo_newproduct').css('width',count);
	
	$('.content.ins #foo_recommend li.mrg').css('margin-right','0');
	$('.content.mp .shnBox').jScrollPane({
		showArrows:true,
		horizontalGutter:20,
		horizontalDragMaxWidth:179
	});
	
	
	function DeleteFromCart(element) {
// $(element).parents('tr').remove();
// setTimeout(function(element) { $(element).parents('tr').remove() }, 300)
	$(element).parents('tr').animate({"height":0+"px","opacity":0,"overflow":"hidden","display":"none"}, 300);
	$(element).parents('tr').find("td").animate({"height":0+"px","padding":0+"px"}, 300);
	$(element).parents('tr').find("td").text('').remove();
	var href = element.href;  
	if (href)               
		$.get( href);     

	return false;
}

	$('#showFilter').click(function(e) {
		var position = $('.content').offset();
		var position_2 = $('#showFilter').offset();
		$('.sFilter').css('top',position_2.top-position.top+41);
	    $('.sFilter').toggle();
	});

$('.bx_slide li span').click(function(e) {
	//alert($(this).css('background-image'));
	$('.bx_bigimages_imgcontainer img').attr('src',$(this).attr('rel'));
});

$('.jq-checkbox').click(function(){
	$('.jq-checkbox.checked').next('label').addClass('act');
})

	
$('.search-suggest').keyup(function(e) {	
$.post( "/include/search.php",{q:this.value}, function( data ) {
													if($('.search-suggest').val()!=''){	
													if(data!=''){var header='<li class="first">Быстрый поиск, первые 6 позиций...</li>';$('.headerMiddleBlockInner .search input.submit,.headerMiddleBlockInner .search input.search-suggest').css('border-bottom','1px solid #e0e0e0');}else{var header='';$('.headerMiddleBlockInner .search input.submit,.headerMiddleBlockInner .search input.search-suggest').css('border','none');}
				$( "#res" ).html(header + data );
				
													}
													else
													{
				$('.headerMiddleBlockInner .search input.submit,.headerMiddleBlockInner .search input.search-suggest').css('border','none');
													$('#res').empty();
													}
			});
});			

/*	$('.sFilter label').on('click',function(){
		$(this).toggleClass('active');
	});
*/
						
})

function addToCart(element, mode, text, type){
		if (!element && !element.href)
		return;
	
		var href = element.href;	
		var button = $(element);
		titleItem = button.parents(".C3PO").find(".item_title").attr('title');
		imgItem = button.parents(".C3PO").find(".item_img").attr('src');	
		$('#addItemInCart .item_title').text(titleItem);
		$('#addItemInCart .item_img img').attr('src', imgItem); 
		var ModalName = $('#addItemInCart');
		CentriredModalWindow(ModalName);
		OpenModalWindow(ModalName);
		
		
		
		if (href)
		$.get( href+"&ajax_buy=1", $.proxy(
	  		function(data) {          
				$.post( "/include/addToCart.php", function( data ) {
				$( "#cart_line" ).html( data );
				var el = document.createElement( 'html' );
				el.innerHTML = data;
				$("#ant_bask_link").html('<a href="http://salda.ru/personal/cart/" class="">Корзина</a><div class="ant_count_label">'+$('#kolvo_in_cart b', el).text()+'</div>');
				$("#img_cart").css("top","-21px")
			}); 
			}) 
		); 
	
	return false;
	}
(function($) {

$(function() {  
  $(".jspContainer").attr("style","").removeClass("jspContainer");
  $(".jspPane").attr("style","").removeClass("jspPane");
  $('.elCount select,.sFilter input[type="checkbox"]').styler();
  var text1 = $("#cart_line").text();
   console.log("a"+text1.replace(/\s+/g,' ')+"b");
  
})  
})(jQuery)