/*
 * Translated default messages for the jQuery validation plugin.
 * Locale: AR (Arabic; العربية)
 */
(function($) {
    var phoneErrorMessage = 'يجب ان تكون صيغة الجوال صحيحة';
	$.extend($.validator.messages, {
		required: 'يجب إدخال القيمة',
		remote: "يرجى تصحيح هذا الحقل للمتابعة",
		email: 'يجب ان يكون الإيميل بهذه الصيغة: "email@domain.com"',
		url: "رجاء إدخال عنوان موقع إلكتروني صحيح",
		date: "رجاء إدخال تاريخ صحيح",
		dateISO: "رجاء إدخال تاريخ صحيح (ISO)",
		number: "رجاء إدخال عدد بطريقة صحيحة",
		digits: "عذراً , لا يمكن قبول الحروف والأرقام الكسريه",
		creditcard: "رجاء إدخال رقم بطاقة ائتمان صحيح",
		equalTo: "رجاء إدخال نفس القيمة",
		extension: "رجاء إدخال ملف بامتداد موافق عليه",
		maxlength: $.validator.format("الحد الأقصى لعدد الحروف هو {0}"),
		minlength: $.validator.format('هذه القيمة قصيرة جدا. يجب أن تكون {0} أحرف أو أكثر.'),
		rangelength: $.validator.format("عدد الحروف يجب أن يكون بين {0} و {1}"),
		range: $.validator.format("رجاء إدخال عدد قيمته بين {0} و {1}"),
		min: $.validator.format("عذراً, اقل قيمة ممكنه هي  {0}"),
		max: $.validator.format("عذرا,ً اكبر قيمة ممكنه  هي {0}"),
                mincheck: $.validator.format('رجاء إختيار عدد أكبر من أو يساوي {0}'),
                password: 'يجب ان تكون كلمة المرور مكونه من 8 خانات وتحتوي على ارقام وحروف',
                passwordMax: 'يجب ان تكون كلمة المرور مكونه من 4096 خانه على الأكثر وتحتوي على ارقام وحروف',
                'phone-international': phoneErrorMessage,
                phone: phoneErrorMessage,
                filesize: $.validator.format('يجب الا يزيد حجم الصوره عن {0} ميجا'),
                dimensions: 'يجب الا تقل ابعاد الصورة عن 200*200',
                coverdimensions: 'يجب الا تقل ابعاد الصورة عن 1920*200',
                unique: "غير متاح",
                terms: 'يجب الموافقة على الشروط والأحكام  ',
                staffUsername:'القيمة المسموح بها حروف و ارقام و شُرط فقط',
                slug:'القيمه المسموح بها حروف و شُرَط بالانجليزية فقط',
                hashtag: 'القيمه غير صحيحة',
                title: 'القيمة المسموح بها حروف و ارقام و شُرط و مسافات  فقط',
                dateAfterToday: 'يجب ان يكون تاريخ الانتهاء بعد تاريخ اليوم',
                tagMincheck: 'يجب ادخال كلمه مفتاحيه واحده على اﻷقل',
                hobbyMincheck: 'هذه القيمة قصيرة جدا. يجب أن تكون 3 أحرف أو أكثر',
                lessthan: 'القيمة غير صحيحه . يجب ان تكون اكبر من "اقل عدد حروف للتعليق"',
		integer: ' هذه القيمة يجب ان تكون من نوع رقم. ',
                duplicate: 'مكرر',
                seodimension:'يجب الا تقل ابعاد الصورة عن 250*205',
                logosize: 'يجب الا يزيد حجم الصوره عن 1 ميجا',
                contactMessage: 'عفوا يوجد خطا فى رقم التتبع برجاء مراجعة رسائل أنتمي و التأكد من رقم التتبع او من حالة الرساله',
                hashtaglesslength: $.validator.format('الوسم يجب أن يكون 3 أحرف أو أكثر.'),
                taglength: $.validator.format('الكلمه المفتاحيه يجب أن تكون 330 حرف أو اقل.'),
                hobbylength: $.validator.format('الحد الأقصى لعدد الحروف هو 200'),
                numberonly:'القيمة المسموح بها أرقام فقط',
                numberMaxlength: 'الحد الأقصى لعدد الأرقام هو 3',
                largerThanCurrentTime: 'لا يمكن إختيار وقت منتهِ ',
                accept: 'رجاء إدخال ملف بامتداد موافق عليه'
	});
}(jQuery));