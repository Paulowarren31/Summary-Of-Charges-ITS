$(function(){
  $('#main-form').submit( () => {

    unit = $('input[name=unit_radio]:checked').attr('id')
    $('#d_choice_id').val(unit)


    date = $('input[name=date_radio]:checked').attr('id')

    if(date == 'date-switch'){
      year = $('#year').val()
      if($('input[name=fc_choice]:checked').length == 1){
        //cal yr
        $('#c_yr_in').val(year)
        $('#t_choice_id').val(2)
      }
      else{
        $('#f_yr_in').val(year)
        $('#t_choice_id').val(1)
        //f yr
      }
    }
    else{
      $('#t_choice_id').val(3)
    }


    return true

  })
  $('#date-switch').on('click', e => {

    if($('#fy-tag').hasClass('bold')){
      $('#fy-tag').removeClass('bold')
      $('#c-tag').addClass('bold')
    }
    else{
      $('#c-tag').removeClass('bold')
      $('#fy-tag').addClass('bold')
    }
  })

})    
