$(function(){
  $('#submit-btn').on('click', function(){
    unit_choice = $("input[name='radio']:checked")[0].id
    if(unit_choice == 'mult-id'){
      ids = $('#mult-id-input').val().split('-')
      min = ids[0]
      max = ids[1]

      if(!min || !max){
        alert('invalid input')
      }
      console.log(min, max)


      /*$.ajax({
        type: 'POST',
        headers: { "X-CSRFToken": $.cookie("csrftoken") },
        url: '/table/',
        data: {
          min: min, 
          max: max,
          type1: 1,
          type2: 0,
          fiscal_yr: 2016,
        },
      })
      */
    }

  })
})
