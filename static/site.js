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