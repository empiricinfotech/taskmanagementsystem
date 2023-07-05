
function displayToast(message) {
    const toastContainer = document.getElementById('toastContainer');
  

    const toast = document.createElement('div');
    toast.className = 'bg-green-500 text-white py-2 px-4 rounded-md shadow';
    toast.innerText = message;
  
    toastContainer.appendChild(toast);

    setTimeout(() => {
      toast.remove();
    }, 3000);
  }


function displayErrorToast(message) {
    const toastContainer = document.getElementById('toastContainer');

    const toast = document.createElement('div');
    toast.className = 'bg-red-500 text-white py-2 px-4 rounded-md shadow';
    toast.innerText = message;

    toastContainer.appendChild(toast);
  
    setTimeout(() => {
      toast.remove();
    }, 3000);
  }

function datachange(e){
    var done = document.getElementById('update_pen'+e)
    var edit=document.getElementById('edit_data'+e);
    var assignTo=document.getElementById('span_assign_To_'+e);
    var assignToDrop=document.getElementById('assign_To_'+e);
    var statusDrop=document.getElementById('status_'+e);
    var priorityDrop=document.getElementById('priority_'+e);
    var progressDrop=document.getElementById('progress_'+e);
    done.classList.add('hidden')
    assignTo.classList.add('hidden')
    edit.classList.remove('hidden')
    assignToDrop.classList.remove('hidden')
    statusDrop.removeAttribute("disabled");
    priorityDrop.removeAttribute("disabled");
    progressDrop.removeAttribute("disabled");
}


function postchange(e){
    var done = document.getElementById('update_pen'+e)
    var edit=document.getElementById('edit_data'+e);
    var assignTo=document.getElementById('span_assign_To_'+e);
    var assignToDrop=document.getElementById('assign_To_'+e);
    var statusDrop=document.getElementById('status_'+e);
    var priorityDrop=document.getElementById('priority_'+e); 
    var progressDrop=document.getElementById('progress_'+e);  
    assign_Value = document.getElementById('assign_To_'+e).value;
    priority_Value = document.getElementById('priority_'+e).value;
    status_Value = document.getElementById('status_'+e).value;
    search_value = document.getElementById('searchIn').value;
    progress_Value = document.getElementById('progress_'+e).value;
    $.ajax({
        type: "POST",
        url: "/tasklist/",
        data: {
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            searchIn:search_value,
            assign:assign_Value,
            priority:priority_Value,
            status:status_Value,
            progress:progress_Value,
            id:e
        },
        success: function(){
            done.classList.remove('hidden')
            document.getElementById('span_assign_To_'+e).classList.remove('hidden')
            document.getElementById('edit_data'+e).classList.add('hidden')
            document.getElementById('assign_To_'+e).classList.add('hidden')
            document.getElementById('status_'+e).setAttribute("disabled",true);
            document.getElementById('priority_'+e).setAttribute("disabled",true);
            document.getElementById('progress_'+e).setAttribute("disabled",true);
            document.getElementById('span_assign_To_'+e).innerHTML=assign_Value
            displayToast('Task Updated successfully !');
        },
        error: function () {
            displayErrorToast("can't Update Task !");
           }
    });      
}

document.getElementById("createTask").onclick = function() { 
    document.getElementById('postData').onclick = function() { 
        var title = document.getElementById('task_title').value;
        var assign_To = document.getElementById('assign_To').value;
        var startdate = document.getElementById('startdate').value;
        var enddate = document.getElementById('enddate').value;
        var status_choice = document.getElementById('status_choice').value;
        var progress_choice= document.getElementById('progress_choice').value;
        var priorities = document.getElementById('priorities').value;
        var dependencies = document.getElementById('tasksdepn').value;
        var Desc = document.getElementById('Desc').value;
        var formData = new FormData();
        formData.append('task_title', title);
        formData.append('assign_To', assign_To);
        formData.append('startdate', startdate);
        formData.append('enddate', enddate);
        formData.append('status_choice', status_choice);
        formData.append('progress_choice', progress_choice);
        formData.append('Desc', Desc);
        formData.append('priorities', priorities);
        formData.append('dependencies', dependencies);
        var files = $('#file_input')[0].files;
        image = $('#file_input')[0].files;
        for (var i = 0; i < files.length; i++) {
            formData.append('upload', files[i]);
        }
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        $.ajax({ 
            type: "POST",
            url: "/tasklist/",
            headers: {'X-CSRFToken': csrftoken},
            data: formData,
            contentType: false,
            processData: false,
            success: function(){
                displayToast('Task Created successfully !');
                document.getElementById("createTaskForm").reset();
                window.location.href = "/tasklist"
            },
            error: function(){
                displayErrorToast("can't Create Task !");
                document.getElementById("createTaskForm").reset();
            }
        });

    }
}


  