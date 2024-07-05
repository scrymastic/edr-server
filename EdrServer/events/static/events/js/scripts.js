document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar-info');
    const sidebarInfoJson = document.querySelector('.sidebar-info-json');
    const eventsTable = document.getElementById('events-table');
    const paginationDiv = document.querySelector('.table-pagination');

    const fetchRowData = (url, universalId) => {
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: `universal_id=${universalId}`
        })
        .then(response => response.json())
        .then(data => {
            sidebarInfoJson.textContent = JSON.stringify(data, null, 2);
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


    const attachRowClickEvent = () => {
        document.querySelectorAll('tbody tr').forEach(row => {
            row.addEventListener('click', (e) => {
                if (e.target.type === 'checkbox') return;
                e.stopPropagation();
                const [, universalId] = row.id.split('/');
                const url = row.getAttribute('action');
                fetchRowData(url, universalId);
            });
        });
    };

    // Search events functionality
    const setupSearch = () => {
        const searchForm = document.getElementById('search-form');

        if (searchForm) {
            searchForm.addEventListener('submit', (e) => {
                e.preventDefault();
                performSearch();
            });
        }
    };

    const performSearch = () => {
        const searchInput = document.getElementById('search');
        const searchForm = document.getElementById('search-form');
        const searchQuery = searchInput.value;
        const url = searchForm.getAttribute('action');
        fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: `query=${searchQuery}`
            })
            .then(response => response.text())
            .then(html => {
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newTable = doc.getElementById('events-table');
                const newPagination = doc.querySelector('.table-pagination');

                if (newTable) eventsTable.innerHTML = newTable.innerHTML;
                if (newPagination) paginationDiv.innerHTML = newPagination.innerHTML;

                attachRowClickEvent();
            })
            .catch(error => console.error('Error:', error));
    };

    document.addEventListener('click', hideSidebar);
    sidebar.addEventListener('click', (e) => e.stopPropagation());


    // Initialize all functionalities
    attachRowClickEvent();
    setupSearch();
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

