
document.addEventListener('DOMContentLoaded', () => {
    const rulesTable = document.getElementById('rules-table');
    const paginationDiv = document.querySelector('.table-pagination');

    // Dropdown functionality
    document.addEventListener('click', (e) => {
        if (e.target.closest('.dropdown')) {
            e.stopPropagation();
            const clickedDropdown = e.target.closest('.dropdown');
            document.querySelectorAll('.dropdown-content').forEach(content => {
                if (content !== clickedDropdown.querySelector('.dropdown-content')) {
                    content.style.display = 'none';
                }
            });
            clickedDropdown.querySelector('.dropdown-content').style.display = 
                clickedDropdown.querySelector('.dropdown-content').style.display === 'block' ? 'none' : 'block';
        } else {
            document.querySelectorAll('.dropdown-content').forEach(content => {
                content.style.display = 'none';
            });
        }
    });

    // Rule editing functionality
    const setupRuleEdit = () => {
        const yamlContent = document.getElementById('yaml-content');
        const editButton = document.getElementById('edit-button');
        const updateButton = document.getElementById('update-button');
        const cancelButton = document.getElementById('cancel-button');

        if (editButton) {
            editButton.addEventListener('click', () => {
                yamlContent.readOnly = false;
                updateButton.disabled = false;
                cancelButton.disabled = false;
            });
        }

        if (cancelButton) {
            cancelButton.addEventListener('click', () => {
                window.location.href = '/rules/';
            });
        }
    };

    // Toggle rule deployment
    const handleRuleToggle = (e) => {
        if (e.target.classList.contains('toggle-rule')) {
            const tr = e.target.closest('tr');
            const ruleId = tr.id.split('/')[1];
            const isActive = e.target.checked;
            const url = e.target.getAttribute('action');

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: `rule_id=${ruleId}&is_active=${isActive}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert(isActive ? 'Rule enabled' : 'Rule disabled');
                } else {
                    alert(isActive ? 'Failed to enable rule' : 'Failed to disable rule');
                    e.target.checked = !isActive;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred');
                e.target.checked = !isActive;
            });
        }
    };

    // Delete rule functionality
    const handleRuleDelete = (e) => {
        if (e.target.classList.contains('delete-rule')) {
            const tr = e.target.closest('tr');
            const ruleId = tr.id.split('/')[1];
            const url = e.target.getAttribute('action');

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: `rule_id=${ruleId}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Rule deleted');
                    tr.remove();
                } else {
                    alert('Failed to delete rule');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred');
            });
        }
    };

    // Update rule functionality
    const setupRuleUpdate = () => {
        const updateButton = document.getElementById('update-button');
        const yamlContent = document.getElementById('yaml-content');
        const ruleContainer = document.querySelector('.rule-container');

        if (updateButton && ruleContainer) {
            const ruleId = ruleContainer.id.split('/')[1];
            updateButton.addEventListener('click', () => {
                const url = updateButton.getAttribute('action');
                const yaml = yamlContent.value;

                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: `rule_id=${ruleId}&yaml=${encodeURIComponent(yaml)}`
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.info);
                    if (data.status === 'success') {
                        window.location.reload();
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred');
                });
            });
        }
    };

    // Create rule functionality
    const setupRuleCreate = () => {
        const addButton = document.getElementById('add-button');
        const yamlContent = document.getElementById('yaml-content');

        if (addButton) {
            addButton.addEventListener('click', () => {
                const url = addButton.getAttribute('action');
                const yaml = yamlContent.value;

                fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: `yaml=${encodeURIComponent(yaml)}`
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.info);
                    if (data.status === 'success') {
                        window.location.href = '/rules/';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred');
                });
            });
        }
    };

    // Search rules functionality
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
                const newTable = doc.getElementById('rules-table');
                const newPagination = doc.querySelector('.table-pagination');

                if (newTable) rulesTable.innerHTML = newTable.innerHTML;
                if (newPagination) paginationDiv.innerHTML = newPagination.innerHTML;

                attachEventListeners();
            })
            .catch(error => console.error('Error:', error));
    };

    const attachEventListeners = () => {
        document.querySelectorAll('.toggle-rule').forEach(toggle => {
            toggle.addEventListener('change', handleRuleToggle);
        });
        document.querySelectorAll('.delete-rule').forEach(deleteButton => {
            deleteButton.addEventListener('click', handleRuleDelete);
        });
    };


    // Initialize all functionalities
    setupRuleEdit();
    setupRuleUpdate();
    setupRuleCreate();
    setupSearch();
    attachEventListeners();
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

