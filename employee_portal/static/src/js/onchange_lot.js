function onchange_product_lot(product)
{
    $.ajax
    ({
    type: 'POST',
    url: '/onchange/product_lotID/',
    dataType: 'json',
    data : {'product': product.value}
    }).done(function(data){
        model = $('#lot_id').empty();
        model_data = '<option value="" style="display:none"> ---Select An Option--- </option>';
        if (data.length != null){
        for(i=0;i<data.length; i++){
            model_data+='<option value="'+data[i].id+'">'+data[i].value+'</option>'
            }
        }
        model.append(model_data);
    });
}


