function showAll(){
    var elements = document.querySelectorAll('.hidden-input');
    console.log("elements",elements)
    for (var i = 0; i < elements.length; i++) {
      var element = elements[i];
      
      element.removeAttribute('hidden');
    }

    var elements2 = document.getElementsByClassName("show-input");
    for (var i = 0; i < elements2.length; i++) {
        var element = elements2[i];
        element.classList.add("hidden");
      }
}

function editData(e){
    console.log("heree-----")
    var title = document.getElementById('task_title').value;
    var status_choice = document.getElementById('status').value;
    var priorities = document.getElementById('priority').value;
    var Desc = document.getElementById('descr').value;
    var assign_To = document.getElementById('assignTo').value;
    var startdate = document.getElementById('startdate').value;
    var enddate = document.getElementById('duedate').value;
    var dependencies = document.getElementById('tasksdepn').value;
    var formData = new FormData();
    formData.append('task_title', title);
    formData.append('id', e);
    formData.append('status_choice', status_choice);
    formData.append('priorities', priorities);
    formData.append('Desc', Desc);
    formData.append('assign', assign_To);
    formData.append('startdate', startdate);
    formData.append('duedate', enddate);
    formData.append('dependencies', dependencies);
    var fileInput = document.getElementById("file_input");
    if (fileInput.files.length > 0) {
        var files = $('#file_input')[0].files;
        image = $('#file_input')[0].files;
        for (var i = 0; i < files.length; i++) {
            formData.append('upload', files[i]);
            console.log("--------file",files[i])
        }
    }

    console.log("--------------images",formData)
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    $.ajax({ 
        type: "POST",
        url: "/tasklist/",
        headers: {'X-CSRFToken': csrftoken},
        data: formData,
        contentType: false,
        processData: false,
        success: function(){
            console.log("success")
            window.location.reload();
        },
        error: function(){
            console.log("error")
            window.location.reload();
        }
    });     
}


const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

const deleteIcons = document.querySelectorAll('.delete-icon');
deleteIcons.forEach(icon => {
  icon.addEventListener('click', () => {
    const imageId = icon.dataset.imageId;

    fetch(`/image/${imageId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken,
      },
    })
    .then(response => response.json())
    .then(data => {
      if (data.success) {
        console.log("--------------- to delete image")
        const imageElement = icon.closest('.relative');
        imageElement.remove();
      } else {
        console.log('Failed to delete image');
      }
    })
    .catch(error => {
      console.log('Error:', error);
    });
  });
});