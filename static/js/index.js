$(function(){
  $('#main-form').submit( () => {
    choices = $('a[class="nav-link active"]')

    choice1 = $(choices[0]).attr('id')
    choice2 = $(choices[1]).attr('id')

    $('#choice1').val(choice1)
    $('#choice2').val(choice2)
    return true
  })
})    
