function get_text(){
    var item_type = document.getElementById('item_type').value
    $.ajax({
        url: '/data_received',
        type: 'POST',
        data: {'name': item_type},
    // After the ajax 'POST' call is finished, call the ajax 'GET' function
    }).done(function(){  
        thing() 
        console.log(item_type)
        document.getElementById('item_type').value = ""
    })
}


function thing(){
    $.ajax({
        url: '/data_sent',
        method: 'GET',
        success: function(result){
            print_thing(result)
        }
    })
}

function print_thing(data){
    console.log(data)
}