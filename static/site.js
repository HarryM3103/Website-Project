function thing(){
    $.ajax({
        url: '/data_sent',
        method: 'GET',
        success: function(result){
            console.log(result)
        }
    })
}