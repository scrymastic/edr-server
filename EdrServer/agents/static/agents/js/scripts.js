document.addEventListener('DOMContentLoaded', function() {
    const connectButtons = document.querySelectorAll('.connect-button');
    
    connectButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const agentInfo = this.closest('.agent-info');
            const ipElement = agentInfo.querySelector('.agent-ip');
            const ip = ipElement ? ipElement.textContent.trim() : null;
            const url = this.getAttribute('action');

            if (!ip) {
                console.error('Agent IP not found');
                return;
            }
            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: `agent_ip=${ip}`
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
            })
            .then(data => {
                console.log('Connection request sent successfully:', data);
                // Handle successful response here
            })
            .catch(error => {
                console.error('Error sending connection request:', error);
                // Handle error here
            });
        });
    });
});

// Function to get CSRF token from cookies (needed for Django)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}