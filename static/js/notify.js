document.querySelectorAll('.mark-as-read').forEach(link => {
    link.addEventListener('click', event => {
        const notificationId = link.getAttribute('data-notification-id');
        const taskId = link.getAttribute('data-task-id');
        fetch(`/${notificationId}/markasread/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()},
        })
        .then(response => {
            if (response.ok) {
                window.location.href = '/task/' + taskId;
            }
        });
    });
});

