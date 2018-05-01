var newId = 0;

var new_registration =
"<div class='well registration'> \
<div class='form-group'> \
<label>Conductor Service</label><br> \
<input id='service-%' type='url' onblur='projectAutocomplete(document.getElementById(%), this.value)' name='service' aria-required='true' required='required' class='form-control' placeholder='Enter address of the Conductor Service'> \
</div> \
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
<input type='url' name='repository' id=% class='form-control' placeholder='e.g. https://github.com/'> \
</div> \
<button type='button' id='removebtn' onclick='removeRegistration(this)' class='btn btn-warning btn-sm' style='float:right'>Remove</button> \
<br> \
</div> \
<script src='/static/js/autocomplete.js'></script>"


function duplicate() {
    newId++;
    var $new = new_registration.replace(/%/g, newId);
    $("#00").append($new);
};

function removeRegistration(caller) {
    $(caller).parents('.registration').remove();
};

function add_field() {
    $("#login").append_field('password', PasswordField('password'))(password="Password123");
};
