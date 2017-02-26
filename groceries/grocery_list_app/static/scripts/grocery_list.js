
$('#grocery-form').on('submit', function(event){
    event.preventDefault();
    console.log("form submitted!")  // sanity check
    create_list();
});


function create_list() {
    console.log("create list is working!") // sanity check
    $.ajax({
        url : "grocery_list/", // the endpoint
        type : "POST", // http method
        data : { the_list : $('#food_name').val() }, // data sent with the post request    
    });
};


function success(json) {
    $('#post-text').val(''); // remove the value from the input
    console.log(json); // log the returned json to the console
    $("#talk").prepend("<li><strong>"+json.text+"</strong> - <em> ");
    console.log("success"); // another sanity check
}