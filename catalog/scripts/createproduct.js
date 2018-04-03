$(function () {

  //Hides all the optional fields
  $("#id_quantity").closest("p").hide()
  $("#id_reorder_trigger").closest("p").hide()
  $("#id_reorder_quantity").closest("p").hide()
  $("#id_pid").closest("p").hide()
  $("#id_max_rental_days").closest("p").hide()
  $("#id_retire_date").closest("p").hide()

  //Shows the appropriate optional fields
  if($("#id_type").val() === 'IndividualProduct') {
    $('#id_pid').closest("p").show();
  }
  if($("#id_type").val() === 'BulkProduct') {
    $('#id_quantity').closest("p").show();
    $('#id_reorder_trigger').closest("p").show();
    $('#id_reorder_quantity').closest("p").show();
  }
  if($("#id_type").val() === 'RentalProduct') {
    $('#id_pid').closest("p").show();
    $('#id_max_rental_days').closest("p").show();
    $('#id_retire_date').closest("p").show();
  }

  $("#id_type").on("change", function(){
    //Hides all the optional fields
    $("#id_quantity").closest("p").hide()
    $("#id_reorder_trigger").closest("p").hide()
    $("#id_reorder_quantity").closest("p").hide()
    $("#id_pid").closest("p").hide()
    $("#id_max_rental_days").closest("p").hide()
    $("#id_retire_date").closest("p").hide()

    //Shows the appropriate optional fields
    if($("#id_type").val() === 'IndividualProduct') {
      $('#id_pid').closest("p").show();
    }
    if($("#id_type").val() === 'BulkProduct') {
      $('#id_quantity').closest("p").show();
      $('#id_reorder_trigger').closest("p").show();
      $('#id_reorder_quantity').closest("p").show();
    }
    if($("#id_type").val() === 'RentalProduct') {
      $('#id_pid').closest("p").show();
      $('#id_max_rental_days').closest("p").show();
      $('#id_retire_date').closest("p").show();
    }
  })

})
