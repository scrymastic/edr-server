


$(document).ready(function(){
    $("tbody tr").click(function(e){
        if (e.target.type === "checkbox") {
            return;
        }
        e.stopPropagation(); // Prevent this event from bubbling up to the document

        var idAttr = $(this).attr("id");
        var splitParts = idAttr.split("/");
        var universalId = splitParts[1];
        var url = $(this).attr("action");

        $.ajax({
            url: url,
            data: {
                'universal_id': universalId
            },
            success: function(data) {
                var jsonString = JSON.stringify(data, null, 2); // The second and third arguments add indentation to make the string more readable
                $(".sidebar-info-json").text(jsonString);
                
                // Check if the sidebar is not visible before showing it
                if (!$(".sidebar-info").is(":visible")) {
                    $(".sidebar-info").animate({width: 'toggle'}, 300);
                }
            }
        });
    });

    $(document).click(function(){
        $(".sidebar-info").animate({width: 'hide'}, 300);
    });

    $(".sidebar-info").click(function(e){
        e.stopPropagation(); // Prevent this event from bubbling up to the document
    });
});



var selectAllCheckbox = document.getElementById('select-all');
var checkboxes = document.querySelectorAll('input[name="event_checkbox"]');

// Add a 'change' event listener to the "Select All" checkbox
selectAllCheckbox.addEventListener('change', function(e) {
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = e.target.checked;
    }
});

// Add a 'change' event listener to each individual checkbox
for (var i = 0; i < checkboxes.length; i++) {
    checkboxes[i].addEventListener('change', function(e) {
        if (!e.target.checked) {
            selectAllCheckbox.checked = false;
        } else {
            var allChecked = true;
            for (var j = 0; j < checkboxes.length; j++) {
                if (!checkboxes[j].checked) {
                    allChecked = false;
                    break;
                }
            }
            selectAllCheckbox.checked = allChecked;
        }
    });
}



$(document).ready(function() {
    $('#push-events').click(function() {
        var checkedEvents = [];
        $('input[name="event_checkbox"]:checked').each(function() {
            checkedEvents.push(this.value);
        });

        var numCheckedEvents = checkedEvents.length;
        if (numCheckedEvents === 0) {
            alert('Please select at least one event to push.');
            return;
        }

        var url = $(this).attr('action');

        $.ajax({
            url: url,
            data: {
                'universal_ids': checkedEvents
            },
            success: function(data) {
                alert(data.message);
                // Redirect to the events page
                window.location.href = '/events/';
            }
        });
    });
});