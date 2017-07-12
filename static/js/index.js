$(function(){
  $('#main-form').submit( () => {

    choices = $('a[class="nav-link active"]')

    d_choice = $(choices[0]).attr('id')
    t_choice = $(choices[1]).attr('id')

    $('#d_choice_id').val(d_choice)
    $('#t_choice_id').val(t_choice)
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
