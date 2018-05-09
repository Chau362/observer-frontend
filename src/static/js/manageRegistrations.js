
$(".register, .unregister").click(function(){

    var parameters = {"eventType": $(this).parent().siblings("[name='event']").text(),
                                     "project": $(this).parent().siblings("[name='projectname']").text(),
                                     "projectUrl": $(this).parent().siblings("[name='url']").text(),
                                     "callback": "http://observer/event/"};


    var $button = $(this);
    var service = $(this).parent().parent().parent().parent().prop("title")

    if ($(this).prop("class").includes("unregister")) {
        addr = service.slice(0,-8) + "/delete/"
        $.ajax({
            type: "POST",
            url:  service,
            data: parameters,
            processData: false,
            contentType: "application/json; charset=UTF-8",
            async: false,
            success: function(result, status, xhr){
                console.log(result);
                $button.prop("class", "btn btn-warning register");
                $button.children().prop("class", "glyphicon glyphicon-minus");
            },
            failure: function(xhr, status, error) {
                         console.log(status);
                     },
            complete: function(result, status, xhr){
                    $.post('registration/', status, function(data){console.log(data)});
            },
            timeout: 3000
        });
    }
    else {
        $.ajax({
            type: "POST",
            url:  service,
            data: JSON.stringify(parameters),
            processData: false,
            contentType: "application/json; charset=UTF-8",
            async: false,
            success: function(result, status, xhr){
                $.post('registration/', parameters, function(data){console.log(data)});
                $button.prop("class", "btn btn-success unregister");
                $button.children().prop("class", "glyphicon glyphicon-ok");
            },
            failure: function(xhr, status, error) {
                         console.log(status);
                     },
            complete: function(result, status, xhr){

            },
            timeout: 3000
        });
    };
});


$("#active-btn").click(function(){
    $.post("activate/", function(){
        $("#active-btn").hide();
        $("#stoplabel").hide();
        $("#inactive-btn").show();
        $("#runlabel").show();
    });
});

$("#inactive-btn").click(function(){
    $.post("deactivate/", function(){
            $("#runlabel").hide();
            $("#inactive-btn").hide();
            $("#active-btn").show();
            $("#stoplabel").show();
    });
});

$( '[name="strikeoutbtn"]' ).click(function() {
    if ($(this).attr("name") == "strikeoutbtn"){
        $(this).parent().parent().attr("class", "strikeout");
        $(this).parent().parent().children("input").attr("disabled", "true");
        $(this).attr("class", "btn btn-warning");
        $(this).attr("name", "cancelbtn");
        $(this).children().attr("class", "glyphicon glyphicon-remove");
    }
    else {
        $(this).parent().parent().attr("class", null);
        $(this).parent().parent().children("input").removeAttr("disabled");
        $(this).attr("class", "btn btn-danger");
        $(this).attr("name", "strikeoutbtn");
        $(this).children().attr("class", "glyphicon glyphicon-trash");
    };
});