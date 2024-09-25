$('#sendComment').click(function (){
    var btn = $(this);
    $.ajax(btn.data('url'), {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': {
            'text': $('#commentText').val(),
        },
        'success': function (response){
            document.getElementById('comments').innerHTML += `<p>${$('#commentText').val()}</p>`;
        }
    })
})