function debounce(func, wait, immediate) {
	var timeout;
	return function() {
		var context = this, args = arguments;
		var later = function() {
			timeout = null;
			if (!immediate) func.apply(context, args);
		};
		var callNow = immediate && !timeout;
		clearTimeout(timeout);
		timeout = setTimeout(later, wait);
		if (callNow) func.apply(context, args);
	};
};

// $('#description').keyup(debounce(function (e) {
//     // e.preventDefault();
//     console.log('submited');
//     console.log($('#form_classifier').serialize());
//     $.ajax({
//         url: 'http://127.0.0.1:8000/order/',
//         type: 'get',
//         dataType: 'json',
//         data: $('#form_classifier').serialize(),
//         beforeSend: function () {
//             $('#loader').show();
//         },
//         complete: function () {
//             $('#loader').hide();
//         },
//         success: function (data) {
//             console.log(data)
//             $('#descriptionValue').html(data['description']);
//             $('#corretiva').html(data['corretiva'].toFixed(2)+" %");
//             $('#melhoria').html(data['melhoria'].toFixed(2)+" %");
//         },
//         error: function (err) {
//             console.log(err)
//         }
//     });
// },500));

function sendOrder(description) {
    return $.ajax({
        url: 'http://127.0.0.1:8000/order/',
        type: 'post',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({ description }),
    });
}

function checkResult(order_id, callback) {
    $.ajax({
        url: `http://127.0.0.1:8000/order/result/${order_id}`,
        type: 'get',
        dataType: 'json',
        success: function (data) {
            if (data.corretiva !== undefined) {
                callback(data);
            } else {
                // resultado ainda não disponível, tenta de novo depois
                setTimeout(() => checkResult(order_id, callback), 1000);
            }
        },
        error: function (err) {
            console.log('Erro ao buscar resultado:', err);
        }
    });
}

$('#description').keyup(debounce(function () {
    const description = $('#description').val();
    if (!description.trim()) return;

    $('#loader').show();
    sendOrder(description)
        .then(res => {
            const order_id = res.order_id;
            checkResult(order_id, function (data) {
                $('#loader').hide();
                $('#descriptionValue').html(data['description']);
                $('#corretiva').html(data['corretiva'].toFixed(2) + " %");
                $('#melhoria').html(data['melhoria'].toFixed(2) + " %");
            });
        })
        .catch(err => {
            $('#loader').hide();
            console.log('Erro ao enviar ordem:', err);
        });
}, 500));