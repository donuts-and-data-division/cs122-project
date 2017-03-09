//these resources were helpful in writing the following javascript:
//https://www.youtube.com/watch?v=o6ueQBrcKrs
//https://www.w3schools.com/jsref/met_table_insertrow.asp



//reset dropdowns after selection
$('#id_other, #id_grains, #id_dairy, #id_meat_and_fish, #id_fruits_and_veggies').click(function(){
    $('#id_other, #id_grains, #id_dairy, #id_meat_and_fish, #id_fruits_and_veggies').val(''); //value of your default option
});


function addFoodtoTable(data, food_id) {    
    console.log("We are running addFoodtoTable")
    //access the table
    var table = document.getElementById("food_list_table");

    //create empty row at beginning of table:
    var row = table.insertRow();
    
    //set table ids
    var table_rows = document.getElementById('food_list_table').rows;
    var rowcount = 0
    for (var i = 0; i < table_rows.length; ++i) {
        table_rows[i].id = rowcount
        rowcount += 1 }

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

    //add content to the new cells:
    console.log('data: ', data)
    food.innerHTML = data.food_name;
    console.log('price', data.food_price)
    price_per_quantity.innerHTML = '$' + (data.food_price).toFixed(2) + '/' + data.food_quantity;
    input_price.innerHTML = '$<input type = "text" size=3 id="price_input">'

    button.appendChild(checkmark);
    button.appendChild(removeButton);
}


//remove food from table on remove button click
$('#food_list_table').on('click', '#removebutton', function() {
    $(this).closest('tr').remove();

    //reset table ids
    var table_rows = document.getElementById('food_list_table').rows;
    var rowcount = 0
    for (var i = 0; i < table_rows.length; ++i) {
        table_rows[i].id = rowcount
        rowcount += 1
    }
});


$('#food_list_table').on('click', '#checkmark', function () {
    //get row id for the selected row
    var rc = $(this).parent().parent().attr('id');

    //get the user input value from that row 
    var price = document.querySelectorAll('#price_input')[rc].value;

    //ensure that the input is integer or float
    if ($.isNumeric(price) == false) {
        alert('please enter a number :-)\ne.g. 4 or 4.00')
    }

    //replace the submit field with a smiley after submission
    var table_rows = document.getElementById('food_list_table').rows;
    var table_cells = table_rows[rc].cells;
    var cell = table_cells[2]
    cell.innerHTML = '<img src= "http://i.imgur.com/2MzKVnC.png" id="smiley">'




    //$.ajax({
        //url: '/ajax/update_prices/',
        //data: {'food_id': food_id, 'store_id': store_id, 'user_price': price},
        //dataType: 'json',
        //success: function(data) {
            //addFoodtoTable(data);
           // }
       // });
//});
    //ajax: food_id, store_id, user_price

   //some function that updates the model with the price
});