document.addEventListener('DOMContentLoaded', () => {
    const selectAllCheckbox = document.getElementById('select-all');
    const checkboxes = document.querySelectorAll('input[name="event_checkbox"]');

    const updateSelectAllCheckbox = () => {
        selectAllCheckbox.checked = Array.from(checkboxes).every(cb => cb.checked);
    };


    const setupPushEvents = () => {
        const pushEventsButton = document.getElementById('push-events');

        if (pushEventsButton) {
            pushEventsButton.addEventListener('click', (e) => {
                e.preventDefault();
                performPushEvents();
            });
        }
    };

    const performPushEvents = () => {
        const checkedEvents = Array.from(checkboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.value);
    
        if (checkedEvents.length === 0) {
            alert('Please select at least one event to push.');
            return;
        }
        const pushEventsButton = document.getElementById('push-events');
        const url = pushEventsButton.getAttribute('action');
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: `universal_ids=${checkedEvents.join(',')}`,
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            alert('Error: ' + error.message);
        });
    }

    selectAllCheckbox.addEventListener('change', (e) => {
        checkboxes.forEach(checkbox => checkbox.checked = e.target.checked);
    });

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateSelectAllCheckbox);
    });


    setupPushEvents();

});
