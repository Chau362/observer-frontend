
var $new_registration = $(
"<div class='well registration'> \
<div class='form-row'> \
<div class='form col-md-6'> \
<label>Projectname</label><br> \
<input type='text' class='form-control' placeholder='Projectname'> \
</div> \
<div class='form-group col-md-6'> \
<label >Eventtype</label><br> \
<input type='text' class='form-control' placeholder='Eventtype'> \
</div> \
</div> \
<div class='form-group'> \
<label>URL</label><br> \
<input type='text' class='form-control' placeholder='e.g. https://github.com/'> \
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