$(function(){
  accounts = $('[id^=a][id$=row]')
  accounts.on('click', function(e){
    icon = e.target
    $(icon).toggleClass('fa-minus-circle fa-plus-circle')

    acc = e.target.id.split('-')[1]
    console.log(acc)

    //get all the categories associated with the account
    categories = $("[id^=a-"+acc+"][id$=grp-show]")

    categories.toggleClass('hidden')

    //when toggling off, we wanna also hide the items
    if(categories.hasClass('hidden')){
      //get all items belonging to the categories above
      items = $('[id^=a-'+acc+'][id$=items]')
      items.addClass('hidden')
    }


    //toggle triangle icon
    //$('#acc-i-'+acc_pk).toggleClass('fa-caret-down fa-caret-up')
  })

  categories = $('[id^=a][id$=grp]')

  //on category click, show all items under that category
  categories.on('click', function(e){
    $(e.target).toggleClass('fa-plus-circle fa-minus-circle')

    acc = e.target.id.split('-')[1]
    grp = e.target.id.split('-')[2]
    console.log(acc, grp)

    elt = '#a-'+acc+'-g-'+grp+'-items'

    $(elt).toggleClass('hidden')

  })


  $('#ex-all').on('click', function(e){
    all = $('[id^=a]')
    $(all).removeClass('hidden')
  })

  $('#hd-all').on('click', function(e){
    all = $('[id^=a]')
    $(all).addClass('hidden')
  })

})
