$("#active-btn").click(function(){
    $.post("http://localhost:5000/profile/activate/");
    $("#active-btn").hide();
    $("#inactive-btn").show();
});

$("#inactive-btn").click(function(){
    $("#inactive-btn").hide();
    $("#active-btn").show();
});