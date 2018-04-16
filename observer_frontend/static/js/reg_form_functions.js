
var $new_registration = $(
"<div class='well registration'> \
<div class='row'> \
<div class='form col-md-8'> \
<label>Projectname</label><br> \
<input type='text' name='projectName' class='form-control' placeholder='Projectname'> \
</div> \
<div class='form-group col-md-4'> \
<label >Eventtype</label><br> \
<input type='text' name='eventType' class='form-control' placeholder='Eventtype'> \
</div> \
</div> \
<div class='form-group autocomplete'> \
<label>URL</label><br> \
<input type='url' name='repository' id='repository' class='form-control' placeholder='e.g. https://github.com/'> \
</div> \
<button type='button' id='removebtn' onclick='removeRegistration(this)' class='btn btn-warning btn-sm' style='float:right'>Remove</button> \
<br> \
</div>"
)

function duplicate() {
    $("#00").append($new_registration.clone());
};

function removeRegistration(caller) {
    $(caller).parents('.registration').remove();
};

function add_field() {
    $("#login").append_field('password', PasswordField('password'))(password="Password123");
};
