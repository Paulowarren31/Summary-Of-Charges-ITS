$(function(){
  $('#main-form').submit( () => {

    date = $('input[name=date_radio]:checked').attr('id')

    if(date == 'whole-year'){
      year = $('#year').val()
      if($('input[name=fc_choice]:checked').length == 1){
        //cal yr
        $('#c_yr_in').val(year)
        $('#t_choice_id').val(2)
      }
      else{
        //f yr

        $('#f_yr_in').val(year)
        $('#t_choice_id').val(1)
      }
    }
    else{
      $('#t_choice_id').val(3)
    }


    return true

  })

  $('#date-slide').on('click', e => {

    if($('input[name=fc_choice]:checked').length == 1){
      $('#fy-tag').addClass('bold')
      $('#c-tag').removeClass('bold')
    }
    else{
      $('#c-tag').addClass('bold')
      $('#fy-tag').removeClass('bold')
    }
  })


  $('#submit-dept-btn').on('click', e => {
    console.log(getCookie('csrftoken'))

    let url = 'https://django-example-paulo-test.openshift.dsc.umich.edu/dept_id'
    let dept_ids = $('#id_dept_id_range').val()

    console.log(dept_ids)

    let data = {
      dept_ids: dept_ids,
      csrftoken: getCookie('csrftoken')
    }

    $.post(url, data, res => {
      console.log(res)
    })

  })


})

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = jQuery.trim(cookies[i]);
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
