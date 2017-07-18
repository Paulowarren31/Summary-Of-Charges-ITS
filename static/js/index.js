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
    let dept_ids = $('#id_dept_id_range').val()

    if(prev.length > 0){
      $('#dept_id_range_actual').val( prev + ',' + dept_ids)
    }
    else{

      $('#dept_id_range_actual').val(dept_ids)
    }

    deptUpdate(dept_ids)
  })

  deptUpdate($('#dept_id_range_actual').val())

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
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function deptUpdate(dept_ids){
  let csrftoken = getCookie('csrftoken')

  //required for django
  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });


  let url = 'https://django-example-paulo-test.openshift.dsc.umich.edu/dept_id'

  console.log(dept_ids)

  let data = {
    dept_ids: dept_ids,
  }

  $.post(url, data, depts => {

    console.log(depts)

    depts.list.forEach(dept => {

      let tr = $("<tr></tr>").html("<td>"+dept[0]+"</td><td>"+dept[1]+"</td>")
      $('#dept_ids_table').append(tr)

    })

    $('#id_dept_id_range').val('') //clear the box


  }
}






