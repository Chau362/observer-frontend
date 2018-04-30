
$(".register").click(function(){

    var parameters = JSON.stringify({"eventType": $(this).parent().siblings("[name='event']").text(),
                                     "project": $(this).parent().siblings("[name='projectname']").text(),
                                     "projectUrl": $(this).parent().siblings("[name='url']").text(),
                                     "callback": "http://observer/event/"});


    var $button = $(this);


    $.ajax({
    type: "POST",
    url:  "http://localhost:5000/event/",
    data: parameters,
    contentType: "application/json; charset=UTF-8",
    async: false,
    success: function(result, status, xhr){
        console.log(result);
        $button.prop("class", "btn btn-success unregister");
        $button.children().prop("class", "glyphicon glyphicon-ok");
    },
    failure: function(xhr, status, error) {
                 console.log(xhr.responseText);
             },
    complete: function(result, status, xhr){
            $.post('registration/', status, function(data){console.log(data)});
    },
    timeout: 3000
    });

});


$(".unregister").click(function(){

    var parameters = JSON.stringify({"eventType": $(this).parent().siblings("[name='event']").text(),
                                     "project": $(this).parent().siblings("[name='projectname']").text(),
                                     "projectUrl": $(this).parent().siblings("[name='url']").text(),
                                     "callback": "http://observer/event/"});


    var $button = $(this);


    $.ajax({
    type: "POST",
    url:  "http://localhost:5000/event/",
    data: parameters,
    contentType: "application/json; charset=UTF-8",
    async: false,
    success: function(result, status, xhr){
        console.log(result);
        $button.prop("class", "btn btn-warning register");
        $button.children().prop("class", "glyphicon glyphicon-minus");
    },
    failure: function(xhr, status, error) {
                 console.log(xhr.responseText);
             },
    complete: function(result, status, xhr){
            $.post('registration/', status, function(data){console.log(data)});
    },
    timeout: 3000
    });

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