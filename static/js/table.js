$(function(){

  var $table = $('main-table')
  $table.floatThead();

  account_icons = $('[id^=group][id$=drop]')

  account_icons.on('click', function(e){
    icon = e.target
    $(icon).toggleClass('fa-minus-circle fa-plus-circle')

    acc = e.target.id.split('-')[1]
    console.log(acc)

    //get all the categories associated with the account
    categories = $("[id=item-"+acc+"]")

    categories.toggleClass('hidden')

    //when toggling off, we wanna also hide the items
    if(categories.hasClass('hidden')){
      //get all items belonging to the categories above
      items = $('[id^=item-'+acc+'-]').not('i')
      items.addClass('hidden')
    }


    //toggle triangle icon
    //$('#acc-i-'+acc_pk).toggleClass('fa-caret-down fa-caret-up')
  })

  categories = $('[id^=item][id$=drop]')

  //on category click, show all items under that category
  categories.on('click', function(e){
    $(e.target).toggleClass('fa-plus-circle fa-minus-circle')

    acc = e.target.id.split('-')[1]
    grp = e.target.id.split('-')[2]

    console.log(acc, grp)

    elt = 'item-'+acc+'-'+grp

    $('[id='+elt+']').toggleClass('hidden')

  })

  $('#expand-slide').on('click', e => {


    //expand all
    if($('input[name=ex_choice]:checked').length == 1){
      all = $('[id^=item]').not('[id$=drop]')
      $(all).removeClass('hidden')
      handleToggles('fa-plus-circle')

    }
    //hide all
    else{
      all = $('[id^=item]').not('[id$=drop]')
      $(all).addClass('hidden')
      handleToggles('fa-minus-circle')

    }
  })

})

function handleToggles(cls1){
  toggles = $('[id$=drop]')
  toggles.each((idx, item) => {
    if($(item).hasClass(cls1)){
      $(item).toggleClass('fa-plus-circle fa-minus-circle')
    }
  })
}
