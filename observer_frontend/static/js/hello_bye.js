
function regfunc(username){
    $.ajax({
    type: "POST",
    url: "http://localhost:5000/profile/register/",
    data: username,
    contentType: "application/json; charset=utf-8",
    dataType: "json",
    success: function(username){alert(username);},
    failure: function(errMsg) {
        alert(errMsg);
    }
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
        $(this).attr("class", "btn btn-warning");
        $(this).attr("name", "cancelbtn");
        $(this).children().attr("class", "glyphicon glyphicon-remove");
    }
    else {
        $(this).parent().parent().attr("class", null);
        $(this).attr("class", "btn btn-danger");
        $(this).attr("name", "strikeoutbtn");
        $(this).children().attr("class", "glyphicon glyphicon-trash");
    };
});