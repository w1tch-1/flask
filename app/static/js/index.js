$('#btn').click(function (){
var formData = new FormData();
    formData.append('text', $('#new-post').val());
    formData.append('image', document.getElementById('image').files[0]);
    $.ajax('/add-post', {
        'type': 'POST',
        'async': true,
        'dataType': 'json',
        'data': formData,
        'contentType': false,
        'processData': false,
        'success': function (data){
            document.getElementById('posts').innerHTML += `<h3>${data["post"]}</h3>`;
            document.getElementById('posts').innerHTML += `<img src="${data['image']}">`;
        }
    })
});
