// После загрузки страницы
$(document).ready(function(){

	//onsole.log('Страница загружена');

	// Маска ввода для телефона
	$(".phone_mask").mask("+7(999) 999-9999", {placeholder:"-"}, {autoclear: false});
	//$("#input_phone").mask("(999) 999-9999");

	//// Фокус в поле поиска
	//// НЕ РАБОТАЕТ
	//$('#select_product').on('select2:open', function () {
	//	//$('.select2-search input').prop('focus',true);
	//	$('.select2-search input').focus();
	//});

});