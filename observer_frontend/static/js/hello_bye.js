$("#reg-btn").click(function(){
    $.post("http://localhost:5000/profile/register/", function(){
        location.reload();
    });
});

$("#active-btn").click(function(){
    $.post("http://localhost:5000/profile/activate/", function(){
        $("#active-btn").hide();
        $("#inactive-btn").show();
    });
});

$("#inactive-btn").click(function(){
    $.post("http://localhost:5000/profile/deactivate/", function(){
            $("#inactive-btn").hide();
            $("#active-btn").show();
    });
});