(function ($) {

  "use strict";


  //Hide Loading Box (Preloader)
//		function handlePreloader() {
//			if($('.preloader').length){
//				$('.preloader').delay(200).fadeOut(500);
//			}
//		}


  //Hide Loading Box (Preloader)
  //		if($('.main-slider-six .default-tab-box .tab-btns').length){
  //			$('.main-slider-six .default-tab-box .tab-btns').mCustomScrollbar();
  //		}


  //Update Header Style and Scroll to Top
  function headerStyle() {
    if ($('.main-header').length) {
      var windowpos = $(window).scrollTop();
      var siteHeader = $('.main-header');
      var scrollLink = $('.scroll-to-top');
      if (windowpos >= 250) {
        siteHeader.addClass('fixed-header');
        scrollLink.fadeIn(300);
      } else {
        siteHeader.removeClass('fixed-header');
        scrollLink.fadeOut(300);
      }
    }
  }

  headerStyle();


  //Submenu Dropdown Toggle
  if ($('.main-header li.dropdown ul').length) {
    $('.main-header li.dropdown').append('<div class="dropdown-btn"><span class="fa fa-angle-down"></span></div>');

    //Dropdown Button
    $('.main-header li.dropdown .dropdown-btn').on('click', function () {
      $(this).prev('ul').slideToggle(500);
    });

    //Disable dropdown parent link
    $('.main-header .navigation li.dropdown > a,.hidden-bar .side-menu li.dropdown > a').on('click', function (e) {
      e.preventDefault();
    });
  }


  //Hidden Bar Menu Config
  function hiddenBarMenuConfig() {
    var menuWrap = $('.hidden-bar .side-menu');
    // hidding submenu
    menuWrap.find('.dropdown').children('ul').hide();
    // toggling child ul
    menuWrap.find('li.dropdown > a').each(function () {
      $(this).on('click', function (e) {
        e.preventDefault();
        $(this).parent('li.dropdown').children('ul').slideToggle();

        // adding class to item container
        $(this).parent().toggleClass('open');

        return false;

      });
    });
  }

  hiddenBarMenuConfig();


  //Hidden Sidebar
  if ($('.hidden-bar').length) {
    var hiddenBar = $('.hidden-bar');
    var hiddenBarOpener = $('.hidden-bar-opener');
    var hiddenBarCloser = $('.hidden-bar-closer');
    $('.hidden-bar-wrapper').mCustomScrollbar();

    //Show Sidebar
    hiddenBarOpener.on('click', function () {
      hiddenBar.addClass('visible-sidebar');
    });

    //Hide Sidebar
    hiddenBarCloser.on('click', function () {
      hiddenBar.removeClass('visible-sidebar');
    });
  }


  /* ==========================================================================
   When document is Scrollig, do
   ========================================================================== */

  $(window).on('scroll', function () {
    headerStyle();
  });

  $('#Carousel-1, #Carousel-2').carousel();

  $('.owl-carousel').owlCarousel({
    rtl: true,
    loop: true,
    margin: 10,
    arrow: true,
    autoplay: true,
    autoplayTimeout: 2000,
    autoplayHoverPause: true,
    nav: true,
    navText: ["<i class='flaticon-right-arrow'></i>", "<i class='flaticon-arrows'></i>"],
    responsive: {
      0: {
        items: 1
      },
      500: {
        items: 2
      },
      740: {
        items: 3
      },
      1200: {
        items: 3
      },
      1300: {
        items: 4
      }
    }

  })
  //  slider video
  $(document).ready(function ($) {
    $('.rvs-container').rvslider({
      autoplay: true,
      loop: true
    });
  });
  // pro slider image
  $(document).ready(function ($) {
    $('#example3').sliderPro({
      width: 960,
      height: 500,
      fade: true,
      arrows: true,
      buttons: false,
      fullScreen: true,
      shuffle: true,
      smallSize: 500,
      mediumSize: 1000,
      largeSize: 3000,
      thumbnailArrows: true,
      autoplay: false
    });
  });
  $(document).ready(function ($) {
    $('#example5').sliderPro({
      width: 500,
      aspectRatio: 2.5,
      height: 550,
      orientation: 'horizontal',
      loop: false,
      arrows: true,
      buttons: false,
      thumbnailsPosition: 'left',
      thumbnailPointer: true,
      thumbnailWidth: 250,
      breakpoints: {
        1200: {
          width: 700,
          height: 550,
          thumbnailWidth: 250,

        },
        800: {
          thumbnailsPosition: 'bottom',
          thumbnailWidth: 270,
          thumbnailHeight: 100
        },
        500: {
          thumbnailsPosition: 'bottom',
          thumbnailWidth: 120,
          thumbnailHeight: 50
        }
      },
      responsive: {
        0: {
          width: 700,
          height: 500
        },
        500: {
          width: 700,
          height: 500
        },
        740: {
          width: 400,
          height: 500
        },
        1200: {
          width: 500,
          height: 500
        }
      }
    });
  });
  $(document).ready(function ($) {
    $('#examplecategory').sliderPro({
      width: '100%',
      aspectRatio: 2.5,
      height: 500,
      orientation: 'vertical',
      loop: true,
      arrows: false,
      buttons: false,
      thumbnailsPosition: 'left',
      thumbnailPointer: true,
      thumbnailWidth: 380,
      thumbnailHeight: 90,
      breakpoints: {
        800: {
          thumbnailsPosition: 'bottom',
          thumbnailWidth: 270,
          thumbnailHeight: 100
        },
        500: {
          thumbnailsPosition: 'bottom',
          thumbnailWidth: 120,
          thumbnailHeight: 50,
          aspectRatio: 1,
          orientation: 'horizontal',
        }
      }
    });
  });

  $(document).ready(function ($) {
    $('#example4').sliderPro({
      width: 960,
      height: 400,
      autoHeight: true,
      fade: true,
      updateHash: true
    });

    // instantiate fancybox when a link is clicked
    $('#example4 .sp-lightbox').on('click', function (event) {
      event.preventDefault();

      // check if the clicked link is also used in swiping the slider
      // by checking if the link has the 'sp-swiping' class attached.
      // if the slider is not being swiped, open the lightbox programmatically,
      // at the correct index
      if ($('#example4').hasClass('sp-swiping') === false) {
        $.fancybox.open(this);
      }
    });
  });

  // popup
  $(document).ready(function () {
    $('.popup-gallery').magnificPopup({
      delegate: 'a',
      type: 'image',
      tLoading: 'Loading image #%curr%...',
      mainClass: 'mfp-img-mobile',
      gallery: {
        enabled: true,
        navigateByImgClick: true,
        preload: [0, 1] // Will preload 0 - before current, and 1 after the current image
      },
      image: {
        tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',
        titleSrc: function (item) {
          return item.el.attr('title') + '<small>by Marsel Van Oosten</small>';
        }
      }
    });
  });

  $(document).ready(function () {
    $('.popup-youtube, .popup-vimeo, .popup-gmaps').magnificPopup({
      disableOn: 700,
      type: 'iframe',
      mainClass: 'mfp-fade',
      removalDelay: 160,
      preloader: false,

      fixedContentPos: false
    });
  });

  // resizing fontsize
  $('.p-block h1,.p-block h2,.p-block h3,.p-block h4,.p-block h5,.p-block h6,.p-block address,.p-block pre,.p-block p,.p-block div').jfontsize({
    btnMinusClasseId: '#jfontsize-m2', // Defines the class or id of the decrease button
    btnDefaultClasseId: '#jfontsize-d2', // Defines the class or id of default size button
    btnPlusClasseId: '#jfontsize-p2', // Defines the class or id of the increase button
    btnMinusMaxHits: 1, // How many times the size can be decreased
    btnPlusMaxHits: 5, // How many times the size can be increased
    sizeChange: 5 // Defines the range of change in pixels
  });

  // datapicker
  $(function () {
    $('#datetimepicker6').datetimepicker(
            {
              format: "DD/MM/YYYY"
            });
    $('#datetimepicker7').datetimepicker({
      useCurrent: false, //Important! See issue #1075
      format: "DD/MM/YYYY"
    });
    $("#datetimepicker6").on("dp.change", function (e) {
      $('#datetimepicker7').data("DateTimePicker").minDate(e.date);
    });
    $("#datetimepicker7").on("dp.change", function (e) {
      $('#datetimepicker6').data("DateTimePicker").maxDate(e.date);
    });
  });

  /*----------------------------------------
   Upload btn
   ------------------------------------------*/
  var SITE = SITE || {};

  SITE.fileInputs = function () {
    var $this = $(this),
            $val = $this.val(),
            valArray = $val.split('\\'),
            newVal = valArray[valArray.length - 1],
            $button = $this.siblings('.btn'),
            $fakeFile = $this.siblings('.file-holder');
//  if(newVal !== '') {
//    $button.text('Photo Chosen');
//    if($fakeFile.length === 0) {
//      $button.after('<span class="file-holder">' + newVal + '</span>');
//    } else {
//      $fakeFile.text(newVal);
//    }
//  }
  };


  $('.file-wrapper input[type=file]').bind('change focus click', SITE.fileInputs);

  function readURL(input, event) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      var tmppath = URL.createObjectURL(event.target.files[0]);

      reader.onload = function (e) {
        $('#img-uploaded').attr('src', e.target.result);
        $('input.img-path').val(tmppath);
      }

      reader.readAsDataURL(input.files[0]);
    }
  }

  $(".uploader").change(function (e) {
    readURL(this, e);
  });

//    $('#myForm').validator()
  /* ==========================================================================
   When document is loaded, do
   ========================================================================== */

  // $(window).on('load', function() {
  // 	handlePreloader();
  // });
//     function change()
//        {
//            if (this.value=="open"){
//                this.value = "close";
//                this.text("اظهار ");
//            }
//            else {
//                this.value = "open";
//                this.text("close ");
//            }
//        }

  //toggle button

//     const Btoggle = document.querySelector('.btn-toggle ')
//    Btoggle.addEventListener('click', function () {
//
//            //toggle button text
//            if (Btoggle.innerHTML==="اخفاء النتائج"){
//                Btoggle.innerHTML = "اظهار النتائج"
//            }
//            else {
//                Btoggle.innerHTML = "اخفاء النتائج"
//            };
//        })
//
//     $('[data-toggle="tooltip"]').tooltip({trigger: 'manual'}).tooltip('show');
//

//	$(window).on('load', function() {
//		handlePreloader();
//	});

})(window.jQuery);

$(".progress-bar").each(function () {
  each_bar_width = $(this).attr('aria-valuenow');
  $(this).width(each_bar_width + '%');
});
