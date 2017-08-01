$(function(){
  //refill dept table if we are coming back to this form
  if($('#dept_id_range_actual').val().length > 0)
    deptUpdate($('#dept_id_range_actual').val(), () => {});



  //submit event for form, we figure out some stuff for backend
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

  //slider for cal yr or fiscal yr event
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


  //when adding a dept, get the dept descr from server
  $('#submit-dept-btn').on('click', e => {
    let dept_ids = $('#id_dept_id_range').val()

    deptUpdate(dept_ids, () => {
      updateActual(dept_ids)
    })
  })


  //tree add event
  $('[id^=add]').on('click', e => {
    split = e.target.id.split('-')
    scope = split[1]
    val = split[2]
    name = split[3]

    console.log(scope, val)

    var tr = ''

    if(scope == 'd'){
      val = 'd.'+ val
      addDept(val, name, val)
    }
    else if(scope == 'grp'){
      val = 'g.'+ val
      addDept('Dept Grp', name, val)
    }
    else if(scope == 'vp'){
      val = 'v.'+ val
      addDept('VP Grp', name, val)
    }

    updateActual(val)

  })
  $('#tree-search-btn').on('click', e => {
    search = $('#tree-input').val()

    tree(search)
  })


})


//function from django docs to get csrf cookie to do ajax
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

//function from django docs to get csrf cookie to do ajax
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function deptUpdate(dept_ids, callback){
  let csrftoken = getCookie('csrftoken')

  //required for django ajax
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

    if(depts.list.length == 0){
      $("#alert").show()

      setTimeout(() => {
        $("#alert").addClass('fade')
        $("#alert").alert('close')
      }, 5000);
      $('#id_dept_id_range').val('') // clear input

      return
    }

    console.log(depts)

    depts.list = depts.list.sort((a, b) => {
      return a[0] - b[0]
    })

    var tr = ''

    if(depts.list.length > 3){
      addDept(depts.list[0][0] + '-' + depts.list[depts.list.length - 1][0],
        'Range', dept_ids);
    }
    else{
      addDept(depts.list[0][0], depts.list[0][1], dept_ids);
    }

    $('#id_dept_id_range').val('') //clear the box

    if(depts.list.length > 0) callback()

  })
}




function updateActual(string){
  let prev = $('#dept_id_range_actual').val()

  if(prev.length > 0){
    $('#dept_id_range_actual').val( prev + ',' + string)
  }
  else{
    $('#dept_id_range_actual').val(string)
  }
}

function addDept(id, name, rm){

  //gross
  tr = $("<tr></tr>").html("<td>"+ id +"</td><td>"+ name
    + '<i id="remove-'+rm
      +'" class="fa fa-minus-circle float-right" aria-hidden="true"></i></td>')

  $('#dept_ids_table').append(tr)

  $(tr).on('click', e => {
    toRemove = e.target.id.split('-')[1]

    prev = $('#dept_id_range_actual').val().split(',')
    idx = prev.indexOf(toRemove)

    if(idx > -1) prev.splice(idx, 1)

    $('#dept_id_range_actual').val(prev)

    $(e.target.parentNode.parentNode).remove() //remove row
  })

}

function tree(search){
  let csrftoken = getCookie('csrftoken')

  $.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
  });

  let url = 'https://django-example-paulo-test.openshift.dsc.umich.edu/search'

  $.get(url, {search: search}, data => {
    console.log(data)
    $('#tree-div').html(data)
  })


}



