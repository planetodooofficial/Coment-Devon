function onchange_project_task(project)
{
    $.ajax
    ({
    type: 'POST',
    url: '/onchange/project_task/',
    dataType: 'json',
    data : {'project': project.value}
    }).done(function(data){
        model = $('#task_id').empty();
        model_data = '<option value="" style="display:none"> ---Select An Option--- </option>';
        if (data.length != null){
        for(i=0;i<data.length; i++){
            model_data+='<option value="'+data[i].id+'">'+data[i].value+'</option>'
            }
        }
        model.append(model_data);
    });
}