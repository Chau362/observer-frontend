
function regfunc(service, projectname, url, event){
    var parameters =  {"eventType": event, "project": projectname,"projectUrl": url, "callback": "http://localhost:5000/event/"};
//
//    $.ajax({
//    type: "POST",
//    url: service,
//    data: JSON.stringify(parameters),
//    dataType: "json",
//    contentType: "application/json; charset=UTF-8",
//    success: function(id){
//                 console.log(id);
//             },
//    failure: function(errMsg) {
//                 console.log(errMsg);
//                 $("#regButton").hide();
//             },
//    timeout: 3000
//    });

//    $.post(service,
//           JSON.stringify(parameters),
//           function(data, status){
//                var id = data;
//                console.log(data, status)
//           },
//           processData = false);

    var xhr = new XMLHttpRequest();

    xhr.open('POST', service);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status === 200) {
            console.log(xhr.responseText);
        }
        else if (xhr.status !== 200) {
            alert('Request failed.  Returned status of ' + xhr.status);
        }
    };
    xhr.send(JSON.stringify(parameters));

//    $.post("http://localhost:5000/profile/register/", function(){console.log('hello')});
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