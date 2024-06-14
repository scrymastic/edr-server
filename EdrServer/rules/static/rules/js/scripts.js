

$(document).ready(function() {
    // Show dropdown on click and hide all other dropdowns
    $(".dropdown").click(function(e) {
        e.stopPropagation(); // Prevent this event from bubbling up to the document

        // Hide all other dropdowns
        $(".dropdown-content").not($(this).children(".dropdown-content")).hide();

        // Show this dropdown
        $(this).children(".dropdown-content").toggle();
    });

    // Hide dropdown when clicking anywhere else on the page
    $(document).click(function() {
        $(".dropdown-content").hide();
    });
});


// Rule edit
document.addEventListener('DOMContentLoaded', (event) => {
    const yamlContent = document.getElementById('yaml-content');
    const editButton = document.getElementById('edit-button');
    const updateButton = document.getElementById('update-button');
    const cancelButton = document.getElementById('cancel-button');

    editButton.addEventListener('click', () => {
        yamlContent.readOnly = false;
        updateButton.disabled = false;
        cancelButton.disabled = false;
    });

    cancelButton.addEventListener('click', () => {
        cancelButton.addEventListener('click', () => {
            window.location.href = '/rules/';
        });
    });
});




// Deploy, undeploy rules
$(document).ready(function() {
    $('.toggle-rule').change(function() {
        var idAttr = $(this).closest('tr').attr('id');
        var splitParts = idAttr.split("/");
        var ruleId = splitParts[1];
        var isActive = $(this).is(':checked');
        var url = $(this).attr('action');
        $.ajax({
            url: url,
            data: {
                'rule_id': ruleId,
                'is_active': isActive
            },
            success: function(response) {
                if (response.status === 'success') {
                    var message = isActive ? 'Rule enabled' : 'Rule disabled';
                    alert(message);
                }
                else {
                    var message = isActive ? 'Failed to enable rule' : 'Failed to disable rule';
                    alert(message);
                    $(this).prop('checked', !isActive);
                }
            }
        });
    }
    );
});


// Delete rules
$(document).ready(function() {
    $('.delete-rule').click(function() {
        var idAttr = $(this).closest('tr').attr('id');
        var splitIndex = idAttr.split("/");
        var ruleId = splitIndex[1];
        var url = $(this).attr('action');
        $.ajax({
            url: url,
            data: {
                'rule_id': ruleId
            },
            success: function(response) {
                if (response.status === 'success') {
                    alert('Rule deleted');
                    $('#' + idAttr).remove();
                }
                else {
                    alert('Failed to delete rule');
                }
            }
        });
    });
});


// Update rule
document.addEventListener('DOMContentLoaded', (event) => {
    const updateButton = document.getElementById('update-button');
    const cancelButton = document.getElementById('cancel-button');
    const yamlContent = document.getElementById('yaml-content');
    
    var ruleContainer = document.querySelector('.rule-container');
    var idAttr = ruleContainer.id;
    var splitIndex = idAttr.split("/");
    var ruleId = splitIndex[1];

    updateButton.addEventListener('click', () => {
        // Update the rule
        var url = updateButton.getAttribute('action');
        var yaml = yamlContent.value;
        $.ajax({
            url: url,
            data: {
                'rule_id': ruleId,
                'yaml': yaml
            },
            success: function(response) {
                alert(response.info);
                if (response.status === 'success') {
                    window.location.reload();
                }
            }
        });
    });

    cancelButton.addEventListener('click', () => {
        window.location.href = '/rules/';
    });
});


// Create rule
document.addEventListener('DOMContentLoaded', (event) => {
    const addButton = document.getElementById('add-button');
    const cancelButton = document.getElementById('cancel-button');
    const yamlContent = document.getElementById('yaml-content');

    addButton.addEventListener('click', () => {
        // Create the rule
        var url = addButton.getAttribute('action');
        var yaml = yamlContent.value;
        $.ajax({
            url: url,
            data: {
                'yaml': yaml
            },
            success: function(response) {
                alert(response.info);
                if (response.status === 'success') {
                    window.location.href = '/rules/';
                }
            }
        });
    });

    cancelButton.addEventListener('click', () => {
        window.location.href = '/rules/';
    });
});




