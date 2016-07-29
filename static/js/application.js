function getAll(){
    $('#sample').find('input[type=checkbox]').each(function(data){
        $(this).checked(true)
    })
}

function query_host(){
    var host = $(this).val();
    $.ajax({
        url: '/host',
        data: 'hid='+host,
        dataType: 'json',
        type: 'get',
        beforeSend: function(){
            $('#hostmodal').modal()
        },
        success: function(data){
            $('#hostmodal').modal()
        },
        error: function(data){
            $('#host_result').html('加载异常， 请联系管理员')
        }
    });
}

function submit_project(){
    var data = $('#project_form').serialize();
    $.ajax({
        url: '/service',
        data: data,
        dataType: 'json',
        type: 'put',
        success: function(data){
            if (data.result == 0){
                $('#service_result').html('加载异常， 请联系管理员')
            }
        }
    });
}

function servicesave() {
    var data = $('#project_form').serialize();
    $.ajax({
        url: '/service',
        method: 'put',
        data: data,
        dataType: 'json',
        success: function(data){
            if (data['retcode'] > 0 ){
                $('#service_result').html('error: '+ data['result'])

            }else{
                window.location.reload()
            }
        }

    })
}
function query_service(){
        var service = $(this).val();
        $.ajax({
            url: '/service',
            data: 'pid='+service,
            dataType: 'json',
            type: 'get',
            beforeSend: function(){
                $('#servicemodal').modal()
            },
            success: function(data){
                console.log(data);
                $('#servicemodal').modal()
            },
            error: function(data){
                $('#result').html('加载异常， 请联系管理员')
            }
        });
}
