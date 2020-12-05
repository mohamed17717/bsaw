var failCount = 0;
var onLogoutRemoveIds = [];
var reoloadPageForChat = false;

function showLoginPopUp(){}

function showNotification(type, txt) {
    toastr.options.rtl = true;
    toastr.options.positionClass= 'toast-top-right';
    toastr.options.progressBar = true;

    if(type == 'error') {
        toastr.error(txt, "")
    }

    if(type == 'success') {
        toastr.success(txt, "")
    }

}

/**
 * @author Mahmoud Mostafa <mahmoud.mostafa@ibtikar.net.sa>
 * @param {boolean} switchToSameUrl if set the redirect will be to the same page url
 */
function switchView(switchToSameUrl) {
    var switchUrl = homeUrl;
    if (switchToSameUrl) {
        switchUrl = window.location.href;
    }
    window.location = switchViewUrl + '?value=mobile&redirectToUrl=' + encodeURIComponent(switchUrl.replace(window.location.protocol + '//' + site_domain, window.location.protocol + '//' + mobile_site_domain));
}

function scrollToElm(selector, extraOffset) {

    var offset = $(selector).offset();
    extraOffset = typeof extraOffset != "undefined" ? extraOffset : 0;
    if (typeof offset != "undefined" && extraOffset == 0) {
        $(document).scrollTop(offset.top)
    } else if ($(document).scrollTop() > offset.top + extraOffset) {
        $(document).scrollTop(offset.top + extraOffset);
    }
}

function clickElm(selector) {
    if ($(selector).length > 0) {
        $(selector).trigger('click');
    }
}

function showChoicesModal(choicesModalTitle, choicesModalMessage, buttons, onCancelFunction) {

    var $choicesModal = $('#choices-modal');

    $choicesModal.find('.modal-title').html(choicesModalTitle);
    $choicesModal.find('.modal-body').html(choicesModalMessage);


    $choicesModal.find('.modal-footer').html("");
    var $firstButton;
    for (var i in buttons) {
        var btn = buttons[i];
        var attrsString = "";

        for (var key in btn.attrs) {
            var value = btn.attrs[key];
            attrsString += key + '="' + value + '" ';
        }
        var $button = $('<a  target="_self" ' + attrsString + ' onclick="' + btn.clickAction + '">' + btn.textValue + '</a>');

        if (!$firstButton) {
            $firstButton = $button;
        }
        $choicesModal.find('.modal-footer').append($button);
    }
    $choicesModal.modal({keyboard: true});
    $choicesModal.on('shown.bs.modal', function () {
        if ($firstButton && window.location == window.parent.location) {
            $firstButton.focus();
        }
    });
    $choicesModal.modal('show');
    $(".btnPrint").printPage();
    $choicesModal.off('hidden.bs.modal');
    $choicesModal.on('hidden.bs.modal', function (e) {
        if (onCancelFunction)
            onCancelFunction();
    });
}

function htmlEncode(str) {
    return str.replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/'/g, '&#039;').replace(/"/g, '&quot;');
}

function closeDialog() {
    $('#choices-modal').modal('hide');
}

function userStateChange(data, triggerLoginEvent) {
    var data = typeof data == "undefined" ? null : data;
//    $('.alert-danger').remove();
    $('.login-slid-div').slideUp(300);
    if (data) {
        if(data.user.avatar){
            $(".userImage").html('<i><img src="/'+data.user.avatar+'" /></i> ' + data.user.username + '<span class="caret"></span>');// responsive
            $('.dev-user-profile').html('<i><img  class="img-circle dev-profile-image" src="/'+data.user.avatar+'"/></i> '+data.user.username+'<span class="caret"></span>')
        }else{
        $(".userImage").html('<i class="fas fa-user-circle" ></i> ' + data.user.username + '<span class="caret"></span>');// responsive
        $('.dev-user-profile').html('<i class="fas fa-user-circle fa-2x" style="margin-top: 5px;"></i> '+data.user.username+'<span class="caret"></span>')

        }
        $('.dev-anon-container').addClass('hide');
        $('.dev-login-in').removeClass('hide');
        // responsive
        $('.userNotLogged').addClass('hide');
        $('.userLogged').removeClass('hide');
        if (data.user.materialCreate) {
            $('.dev-material-create').removeClass('hide');
        }
        if (data.user.backend) {
            $('.dev-backend-control').removeClass('hide');
        }
        if (data.user.comicsCreate) {
            $('.dev-comics-create').removeClass('hide');
        }
        isLoggedIn = true;
        if (triggerLoginEvent) {
            $(window).trigger('user.loggedin');
        }
        $('.top-note').addClass('hidden');
        for (var variableName in data.injectJSVariables) {
            window[variableName] = data.injectJSVariables[variableName];
        }
        for (var fileId in data.injectFiles) {
            loadScript(data.injectFiles[fileId], null, fileId);
            onLogoutRemoveIds.push(fileId);
        }
        if (typeof afterLoginPerformAction === 'function') {
            afterLoginPerformAction();
            afterLoginPerformAction = null;
        }

//        if($('#login-popup').is(':visible')){
//            lightcase.close();
//        }

    } else {
        $('.dev-user-profile').html("");
//        $('[type="password"]').val("");
        $('.dev-anon-container').removeClass('hide');
        $('.dev-login-in').addClass('hide');
        $('#dev-material-create').addClass('hide');
        $('#dev-backend-control').addClass('hide');
        $('#dev-comics-create').addClass('hide');
        if (typeof timerNotificationsInterval !== 'undefined' && timerNotificationsInterval) {
            clearInterval(timerNotificationsInterval);
        }
        var userStatusLognout = isLoggedIn;
        isLoggedIn = false;
        if (userStatusLognout) {
            $(window).trigger('user.loggedout');
        }
        $('.top-note').removeClass('hidden');
        for (var fileIdIndex in onLogoutRemoveIds) {
            $('#' + onLogoutRemoveIds[fileIdIndex]).remove();
        }
    }
}

function showAuthError(error) {
    if (++failCount >= 3 || error.indexOf("Captcha") != -1) {
        location.href = loginUrl;
    } else {
        showNotification('error',error);
    }
}


function SocialNetworkConnect(element) {
    newWindow = window.open($(element).attr("data-url"), '', 'height=800, width=1000');
    if (window.focus) {
        newWindow.focus();
    }
    timer = setInterval(checkChild, 500);
}
    function checkChild() {
        if (errorMessage != false) {
            if (newWindow.closed) {
                msg = '<div class="alert alert-danger remove-5s">' + socialNetworkErrorMessage + '</div>';
                if ($('.dev-login-li .alert').length > 0) {
                    $('.dev-login-li .alert').remove();
                }
                $('.dev-login-li').prepend(msg);
                clearInterval(timer);
            }
        }
    }

function getprayerTimeData() {
    $.ajax({
        url: getPrayerInfoUrl,
        success: preparePrayerTimeWidget
    });
}
    var min = 16;
    var max = 20;

    function increaseFontSize() {
        var p = $('.details-text');
        for (i = 0; i < p.length; i++) {
            if (p[i].style.fontSize) {
                var s = parseInt(p[i].style.fontSize.replace("px", ""));
            } else {
                var s = 18;
            }
            if (s != max) {
                s += 1;
            }
            p[i].style.fontSize = s + "px"
        }
    }

    function decreaseFontSize() {
        var p = $('.details-text');
        for (i = 0; i < p.length; i++) {
            if (p[i].style.fontSize) {
                var s = parseInt(p[i].style.fontSize.replace("px", ""));
            } else {
                var s = 18;
            }
            if (s != min) {
                s -= 1;
            }
            p[i].style.fontSize = s + "px"
        }
    }

    function resetFontSize() {
        var p = $('.details-text');
        for (i = 0; i < p.length; i++) {
            p[i].style.fontSize = "18px"
        }
    }

    $('body').on('click','.largeFont',function () {
        increaseFontSize();
    });
    $('body').on('click','.smallFont',function () {
        decreaseFontSize();
    });
    $('body').on('click','.normalFont',function () {
        resetFontSize();
    });

    function sharePopup(url, w, h) {
        var left = (screen.width / 2) - (w / 2);
        var top = (screen.height / 2) - (h / 2);
        return window.open(url, "share window", 'toolbar=no, location=no, directories=no, status=no, menubar=no, scrollbars=yes, copyhistory=no, width=' + w + ', height=' + h + ', top=' + top + ', left=' + left);
    }

function loginToChat() {
    $.ajax({
        url: chatLoginUrl,
        success: function (data) {
            if (reoloadPageForChat && data.loggedIn) {
                window.location.reload(true);
                return;
            }
            loadScript('https://repository.chatwee.com/scripts/72e4b84d2ef104b50494d305ab4bde88.js', null, 'chatwee-js-tag');
        }
    });
}

function logoutFromChat() {
    $.ajax({
        url: chatLogoutUrl,
        success: function() {
            $('#chatwee-js-tag').remove();
        }
    });
}


$(document).on('shown.bs.tab', 'a[data-toggle="tab"]',function (e) {
  var target = $(e.target).attr("href") // activated tab
 if(target=='#tab_default_2'){
     setTimeout(function(){
      initFormValidation() ;
     },200)

 }
});
jQuery(document).ready(function ($) {

        $('form[name=searchForm]').submit(function (e) {
        if (typeof inAngularLayout === 'undefined') {
            e.preventDefault();
            $(this).data('submitted', true);
            var searchString = $(this).find('input[name=searchString]').val().trim();
            if (!searchString || searchString.length < 3) {
                $(this).find('.form-group').addClass('input-is-invalid');
                $(this).find('span').show();
            } else {
                window.location = searchPageUrl + '?searchString=' + encodeURIComponent(searchString);
            }
        }
    });
    // the quick search forms inputs validation action
    $('input[name=searchString]').keyup(function () {
        if (typeof inAngularLayout === 'undefined') {
            if ($(this).closest('form').data('submitted')) {
                var searchString = $(this).val().trim();
                if (!searchString || searchString.length < 3) {
                    $(this).parent().addClass('input-is-invalid');
                    $(this).parent().find('span').show();
                } else {
                    $(this).parent().removeClass('input-is-invalid');
                    $(this).parent().find('span').hide();
                }
            }
        }
    });

    $(function () {
        $ds = $('#dev-date-container span');
        $ds.hide().eq(0).show();
        setInterval(function () {
            $ds.filter(':visible').fadeOut(function () {
                var $div = $(this).next('span');
                if ($div.length == 0) {
                    $ds.eq(0).fadeIn();
                } else {
                    $div.fadeIn();
                }
            });
        }, 5000);
    });

    //submenu
    $('.menu-item-section').on('click', function (x, y, z) {
        var menuIndex = $('.menu-item-section').index(this);
        $('.submenu-dropzone').slideUp(300);
        $('.submenu-dropzone').eq(menuIndex).stop(true, false, true).slideToggle(300);
        return false;
    });


    $('body').on('submit', '#ajax-form-login,#ajax-form-login-resp,#ajax-form-login-comment', function (e) {
        e.preventDefault();

//        $('.alert-danger').remove();
        var $this = $(e.currentTarget),
                inputs = {};

        // Send all form's inputs
        $.each($this.find('input'), function (i, item) {
            var $item = $(item);
            if ($item.is(':checkbox')) {
                if ($item.is(':checked'))
                    inputs[$item.attr('name')] = 1;
            } else {
                inputs[$item.attr('name')] = $item.val();
            }
        });

        // Send form into ajax
        if ($(this).valid()) {
            $.ajax({
                url: $this.attr('action'),
                type: 'POST',
                dataType: 'json',
                data: inputs,
                success: function (data) {
                    if (data.has_error) {
                        showAuthError(data.error);
                    } else {
                        window.location.reload();
                    }
                }
            });
        }
    });

getBreakingNews();

function getBreakingNews(){
    $.ajax({
        url: $("#breakingNewsUrl").val(),
        method: 'GET',
        success: function (responseData) {
            $("#breakingNews").html(responseData);
        }
    });
}
});
