//these resources were helpful in writing the following javascript:
//https://www.youtube.com/watch?v=o6ueQBrcKrs
//https://www.w3schools.com/jsref/met_table_insertrow.asp

//get data based on selected food
$('#id_food, #id_other, #id_grains, #id_dairy, #id_meat_and_fish, #id_fruits_and_veggies').change(function () {

    var food_id = $(this).val();
    
    $.ajax({
        url: '/ajax/cash_register/',
        data: {'food_id': food_id},
        dataType: 'json',
        success: function(data) {
            addFoodtoTable(data);
            }
        });
});

//reset dropdowns after selection
$('#id_other, #id_grains, #id_dairy, #id_meat_and_fish, #id_fruits_and_veggies').click(function(){
    $('#id_other, #id_grains, #id_dairy, #id_meat_and_fish, #id_fruits_and_veggies').val(''); //value of your default option
});


function addFoodtoTable(data) {    

    //access the table
    var table = document.getElementById("food_list_table");

    //create empty row at beginning of table:
    var row = table.insertRow();

    //insert cells into the row
    var food = row.insertCell(0);
    var price_per_quantity = row.insertCell(1);
    var input_price = row.insertCell(2);
    var button = row.insertCell(3);

    //create buttons
    var removeButton = document.createElement("button");
    removeButton.innerHTML = "";
    removeButton.id = 'removebutton';

    var checkmark = document.createElement('button');
    checkmark.innerHTML = ''
    checkmark.id = "checkmark"
    checkmark.form = "price_form"

    //add content to the new cells:
    food.innerHTML = data.food_name;
    price_per_quantity.innerHTML = '$' + (data.food_price).toFixed(2) + '/' + data.food_quantity;
    input_price.innerHTML = '<input type = "text" size=4 id="price_input">'
    button.appendChild(checkmark);
    button.appendChild(removeButton);
}


//remove food from table on remove button click
$('#food_list_table').on('click', '#removebutton', function() {
    $(this).closest('tr').remove();
});


$('#food_list_table').on('click', '#checkmark', function () {
    var text = $(this).parent().prev('td');
    alert(text.text());
   //some function that updates the model with the price
});