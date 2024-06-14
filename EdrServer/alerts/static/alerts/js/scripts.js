

$(document).ready(function(){
    $("tbody tr").click(function(e){
        if (e.target.type === "checkbox") {
            return;
        }
        e.stopPropagation(); // Prevent this event from bubbling up to the document

        var idAttr = $(this).attr("id");
        var splitParts = idAttr.split("/");
        var ruleId = splitParts[1];
        var eventUniversalId = splitParts[2];
        var url = $(this).attr("action");

        $.ajax({
            url: url,
            data: {
                'rule_id': ruleId,
                'event_universal_id': eventUniversalId,
            },
            success: function(data) {
                var rule = data['rule'];
                var event = data['event'];
                var jsonString = JSON.stringify(event, null, 2); // The second and third arguments add indentation to make the string more readable
                $(".sidebar-info-link").attr("href", rule['link']);
                $(".sidebar-info-description").text(rule['description']);
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