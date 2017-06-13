$(function(){
  accounts = $('[id^=acc]').not('[id$=cat]').not('[id$=i]')
  accounts.on('click', function(e){
    acc_pk = e.target.parentNode.id.split('-')[1]

    //get all the categories associated with the account
    categories = $('[id^=acc-'+acc_pk+'][id$=cat]').toggleClass('hidden')


    //when toggling off, we wanna also hide the items
    if(categories.hasClass('hidden')){

      //get all items belonging to the categories above
      items = $('[id^=acc-'+acc_pk+'][id$=i]')
      items.addClass('hidden')
    }


    //toggle triangle icon
    $('#acc-i-'+acc_pk).toggleClass('fa-caret-down fa-caret-up')
  })

  categories = $('[id^=acc][id$=cat]')

  //on category click, show all items under that category
  categories.on('click', function(e){
    acc_pk = e.target.parentNode.id.split('-')[1]
    cat_pk = e.target.parentNode.id.split('-')[3]

    //toggle hidden class for all items under a category
    $('[id^=acc-'+acc_pk+'-cat-'+cat_pk+']').not('[id$=cat]').toggleClass('hidden')

    $('#cat-i-'+cat_pk).toggleClass('fa-caret-down fa-caret-up')

  })

})
