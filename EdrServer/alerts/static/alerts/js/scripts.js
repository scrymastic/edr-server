
document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar-info');
    const sidebarTitle = document.querySelector('.sidebar-info-title');
    const sidebarDescription = document.querySelector('.sidebar-info-description');
    const sidebarLink = document.querySelector('.sidebar-info-link');
    const sidebarJson = document.querySelector('.sidebar-info-json');


    const showEventDetails = async (event) => {
        if (event.target.type === 'checkbox') return;
        event.stopPropagation();

        const row = event.currentTarget;
        const [, ruleId, eventUniversalId] = row.id.split('/');
        const url = row.getAttribute('action');

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: `rule_id=${ruleId}&event_universal_id=${eventUniversalId}`
        })
        .then(response => response.json())
        .then(data => {
            sidebarTitle.textContent = data.rule.title;
            sidebarDescription.textContent = data.rule.description;
            sidebarLink.setAttribute('href', `/rules/view_rule/${data.rule.id}`);
            sidebarJson.textContent = JSON.stringify(data.event, null, 2);
            showSidebar();
        })
        .catch(error => console.error('Error:', error));

    };

    const showSidebar = () => {
        if (!sidebar.offsetWidth) {
            sidebar.style.display = 'block';
            sidebar.style.right = '-400px';
            sidebar.offsetWidth;
            sidebar.style.right = '0';
        }
    };

    const hideSidebar = () => {
        if (sidebar.offsetWidth) {
            sidebar.style.right = '-400px';
            setTimeout(() => sidebar.style.display = 'none', 300);
        }
    };


    document.querySelectorAll('tbody tr').forEach(row => {
        row.addEventListener('click', showEventDetails);
    });

    document.addEventListener('click', hideSidebar);
    sidebar.addEventListener('click', (e) => e.stopPropagation());
});


// Utility function to get CSRF token
const getCookie = (name) => {
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
};
