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
  $('#date-slide').on('click', e => {

    if($('input[name=fc_choice]:checked').length == 1){
      $('#c-tag').addClass('bold')
      $('#fy-tag').removeClass('bold')
    }
    else{
      $('#fy-tag').addClass('bold')
      $('#c-tag').removeClass('bold')
    }

  })

})    
