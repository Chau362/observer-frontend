
function regfunc(service, projectname, url, event){
    $.ajax({
    type: "POST",
    url: service,
    data: {
        "eventType": event,
        "project": projectname,
        "projectUrl": url,
        "callback": "http://localhost:5000/event/"
     },
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(id){
                 alert(id);
             },
    failure: function(errMsg) {
                 console.log(errMsg);
                 $("#regButton").hide();
             },
    timeout: 3000
    });
};

$("#active-btn").click(function(){
    $.post("http://localhost:5000/profile/activate/", function(){
        $("#active-btn").hide();
        $("#stoplabel").hide();
        $("#inactive-btn").show();
        $("#runlabel").show();
    });
});

$("#inactive-btn").click(function(){
    $.post("http://localhost:5000/profile/deactivate/", function(){
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