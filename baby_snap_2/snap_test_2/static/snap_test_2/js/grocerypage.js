//these resources were helpful in writing the following javascript:
//https://www.youtube.com/watch?v=o6ueQBrcKrs
//https://www.w3schools.com/jsref/met_table_insertrow.asp

//initialize food ids to list
var food_ids = [];

//get data based on selected food
$('#id_food, #id_other, #id_grains, #id_dairy, #id_meat_and_fish, #id_fruits_and_veggies').change(function () {
    var food_id = $(this).val();
    
    $.ajax({
        url: '/ajax/cash_register/',
        data: {'food_id': food_id},
        dataType: 'json',
        success: function(data) {
            addFoodtoTable(data, food_id);
            food_ids.push(food_id);
            }
        });
});


//reset dropdowns after selection
$('#id_other, #id_grains, #id_dairy, #id_meat_and_fish, #id_fruits_and_veggies').click(function(){
    $('#id_other, #id_grains, #id_dairy, #id_meat_and_fish, #id_fruits_and_veggies').val(''); //value of your default option
});


function addFoodtoTable(data, food_id) {   
  
    //access the table & create empty row at beginning
    var table = document.getElementById("food_list_table");
    var row = table.insertRow();
    
    //insert cells into the row
    var food = row.insertCell(0);
    var price_per_quantity = row.insertCell(1);
    var total_price = row.insertCell(2);
    var quantity = row.insertCell(3);
    var button = row.insertCell(4);
    var this_food_id = row.insertCell(5);
    this_food_id.id = 'invisible'

    //create buttons and assign unique ids to each
    var removeButton = document.createElement("button");
    var increaseButton = document.createElement('button');
    var decreaseButton = document.createElement('button');
    removeButton.id = 'removebutton';
    increaseButton.id = "increaseButton"
    decreaseButton.id = "decreaseButton"
    
    //add content to the new cells:
    this_food_id.innerHTML = food_id
    var input_quantity = 1
    food.innerHTML = data.food_name;
    price_per_quantity.innerHTML = '$' + (data.food_price).toFixed(2) + '/' + data.food_quantity;
    total_price.innerHTML = '$' + (data.food_price * input_quantity).toFixed(2);
    quantity.innerHTML = '<p id = "quantity" >' + input_quantity + '</p>';
    button.appendChild(increaseButton);
    button.appendChild(decreaseButton);
    button.appendChild(removeButton)
    
    //recalculate total price
    updateTotalPrice() 
}


//increase quantity and update price on remove button click
$('#food_list_table').on('click', '#increaseButton', function () {
    var text = $(this).parent().prev('td');
    var new_quant = parseFloat(text.text()) + 0.25;
    text.html(new_quant);
    var per_price = text.prev('td').prev('td').text();
    var float_price = parseFloat(per_price.slice(1));
    var total_price = $(this).parent().prev('td').prev('td')
    var new_amount = float_price * new_quant
    total_price.html('$' + new_amount.toFixed(2));
    
    //recalculate total price
    updateTotalPrice()
});

//decrease quantity and update total price on decrease button click
$('#food_list_table').on('click', '#decreaseButton', function () {
    var text = $(this).parent().prev('td');
    var new_quant = parseFloat(text.text()) - 0.25;
    if (new_quant <= 0) {
        $(this).closest('tr').remove();
        var id = $(this).parent().next('td').text();
        removeFoodID(id)
    }

    text.html(new_quant);
    var per_price = text.prev('td').prev('td').text();
    var float_price = parseFloat(per_price.slice(1));
    var total_price = $(this).parent().prev('td').prev('td')
    var new_amount = float_price * new_quant
    total_price.html('$' + new_amount.toFixed(2));
    
    //recalculate total price
    updateTotalPrice()
      
}); 


//remove food from table and update total price on remove button click
$('#food_list_table').on('click', '#removebutton', function() {
    $(this).closest('tr').remove();

    //remove food id from list
    var id = $(this).parent().next('td').text();
    removeFoodID(id)

    //recalculate total price
    updateTotalPrice()
});


//remove the id from the id list if the user deletes it from the table
function removeFoodID(id) {
    var i = food_ids.indexOf(id)
    if (i!= -1) {
      food_ids.splice(i, 1);
    }
}  


function updateTotalPrice() {
    var table_rows = document.getElementById('food_list_table').rows;
    var new_total = 0
    if (table_rows.length == 0) {
    document.getElementById('total').innerHTML = '$' + parseFloat(0.00);
    }
      
    for (var i = 0; i < table_rows.length; ++i) {
        table_cells = table_rows[i].cells;
        item_amount = table_cells[2].innerHTML;
        float_amount = parseFloat(item_amount.slice(1));
        new_total += float_amount;
    }

    document.getElementById('total').innerHTML = '&nbsp;&nbsp;' + '$' + new_total.toFixed(2);
}

