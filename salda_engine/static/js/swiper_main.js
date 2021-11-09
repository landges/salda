var mySwiper = new Swiper('.swiper-container', {
    slidesPerView: 1,
    loop: true,
    navigation: {
        nextEl: '.flex-next',
        prevEl: '.flex-prev'
    },
    breakpoints: {
        540: {
            slidesPerView: 4
        }
    }

});

$(document).on('click','.swiper-container',function(event){
    var slide=$(event.target).closest('.swiper-slide');
    var current_slide=$("li.current.swiper-slide");
    var current_slide_ind=current_slide.attr('id').slice(-1);
    var big_image_ind=slide.attr('id').slice(-1);
    var big_image_current=slide.closest('.big-slider').find(`li#photo-${current_slide_ind}`);
    var big_image=slide.closest('.big-slider').find(`li#photo-${big_image_ind}`);
    big_image_current.removeClass('current');
    big_image.addClass('current');
    current_slide.removeClass('current');
    slide.addClass("current");
});

var BrandSwiper = new Swiper('.flex-viewport', {
    slidesPerView: 1,
    loop: true,
    navigation: {
        nextEl: '.flex-next',
        prevEl: '.flex-prev'
    },
    breakpoints: {
        540: {
            slidesPerView: 5
        }
    }

});