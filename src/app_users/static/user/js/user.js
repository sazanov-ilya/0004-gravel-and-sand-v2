
// Общие функции
function get_all_cost(){
	// Читаем поля
	let count_unit = parseFloat($('#input_count_unit').val());
	let cost_unit = parseFloat($('#label_cost_unit').val());
	let delivery_cost = parseFloat($('#label_delivery_cost').val());

	// Выводим стоимость
	let all_cost = count_unit * cost_unit + delivery_cost;
	if (isNaN(all_cost)){
		$('#input_all_cost').val(0);
	}
	else{
		$('#input_all_cost').val(all_cost);
	}
	console.log('all_cost: ' + all_cost);
};


// После загрузки страницы
$(document).ready(function(){

	console.log('Страница загружена');

	// подключаем select2 на списки
	$('#select_product').select2({
		theme: "bootstrap-5",
		//containerCssClass: "select2--small", // For Select2 v4.0
		selectionCssClass: "select2--small", // For Select2 v4.1
		//dropdownCssClass: "select2--small",
		placeholder: 'Выберите продукт',
		allowClear: true
	});

	$('#select_area').select2({
		theme: "bootstrap-5",
		//containerCssClass: "select2--small", // For Select2 v4.0
		selectionCssClass: "select2--small", // For Select2 v4.1
		//dropdownCssClass: "select2--small",
		placeholder: "Выберите район доставки",
		allowClear: true
	});

	// Обнуляем поля

	// Timezone
	//const tzid = Intl.DateTimeFormat().resolvedOptions().timeZone;
	//$('#input_timezone').val(tzid); // Europe/Moscow
	$('#input_timezone').val(-(new Date()).getTimezoneOffset() / 60);

	$('#input_count_unit').val(0);
	$('#label_unit').val('нет');
	$('#label_cost_unit').val(0);
	$('#label_delivery_cost').val(0);
	$('#input_all_cost').val(0);

	// Маска ввода для телефона
	$("#input_phone").mask("+7(999) 999-9999", {placeholder:"-"}, {autoclear: false});
	//$("#input_phone").mask("(999) 999-9999");

	//// Фокус в поле поиска
	//// НЕ РАБОТАЕТ
	//$('#select_product').on('select2:open', function () {
	//	//$('.select2-search input').prop('focus',true);
	//	$('.select2-search input').focus();
	//});

	// Выбор продукта
	$('#select_product').on('select2:select', function(){
		let product_id = $("#select_product option:selected").val();
		//let url = '/get_products';
		$.ajax({
		type: "GET", // or POST
		headers: {'X-CSRFToken': "{{ csrf_token }}"},
		datatype: 'json',
		url: '/order/get_products',
		data: {"product_id": product_id},
		success: function(response) {
			//console.log('ajax, успех: ' + response[0].product_name);
			//console.log('ajax, успех: ' + response[0].product_unit);
			//console.log('ajax, успех: ' + response[0].product_price);
			$('#label_unit').val(response[0].product_unit);
			$('#label_cost_unit').val(response[0].product_price);

			// Общая стоимость
			get_all_cost();
		},
		error: function(response){
			console.log(response.responseJSON.errors);
			$('#label_unit').val('нет');
			$('#label_cost_unit').val(0);
			$('#input_all_cost').val(0);
		}
	});
	});

	// Выбор района
	$ ('#select_area').on('select2:select', function(){
		let area_id = $("#select_area option:selected").val();
		//let url = '/get_areas';
		$.ajax({
		type: "GET", // or POST
		headers: {'X-CSRFToken': "{{ csrf_token }}"},
		datatype: 'json',
		url: '/order/get_areas',
		data: {"area_id": area_id},
		success: function(response) {
			//console.log('ajax, успех: ' + response[0].area_name);
			//console.log('ajax, успех: ' + response[0].area_price);
			$('#label_delivery_cost').val(response[0].area_price);

			// Общая стоимость
			get_all_cost();
		},
		error: function(response) {
			console.log(response.responseJSON.errors);
			$('#label_delivery_cost').val(0);
			$('#input_all_cost').val(0);
		}
	});
	});

	// Ввод количества
	$('#input_count_unit').on('input keyup', function(e) {
		// Перерасчет стоимости
		get_all_cost();
	});

});