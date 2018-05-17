
$(".register, .unregister").click(function(){

    var active = $(this).parent().siblings("[name='active']").val() == "false" ? false : true;
    var service = $(this).parent().parent().parent().parent().prop("title")
    var parameters = {'event': $(this).parent().siblings("[name='event']").text(),
                                     'id': $(this).parent().siblings("[name='id']").val(),
                                     'project_name': $(this).parent().siblings("[name='project_name']").text(),
                                     'project_url': $(this).parent().siblings("[name='project_url']").text(),
                                     'service': service,
                                     'active': active};

    var $button = $(this);

    console.log(parameters)

    if ($(this).prop("class").includes("unregister")) {
        $.ajax({
            type: "POST",
            url:  "remove-follow/",
            data: JSON.stringify(parameters),
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
            timeout: 3000
        });
    }
    else {
        $.ajax({
            type: "POST",
            url:  "add-follow/",
            data: JSON.stringify(parameters),
            contentType: "application/json; charset=UTF-8",
            success: function(result, status, xhr){
                console.log(result);
                $button.prop("class", "btn btn-success unregister");
                $button.children().prop("class", "glyphicon glyphicon-ok");
            },
            failure: function(xhr, status, error) {
                console.log(status);
             },
            timeout: 3000
        });
    };
});


$("[name*='btn']").click(function(){
    if ($(this).attr("name") == "pause-btn"){
        $.post("deactivate/", function(){
            location.reload();
        });
    }
    else {
        $.post("activate/", function(){
            location.reload();
        });
    }
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