    const targetDiv = document.getElementById("third");
    const btn = document.getElementById("toggle");
    btn.onclick = function() {
        if (targetDiv.style.display !== "none") {
            targetDiv.style.display = "none";
        } else {
            targetDiv.style.display = "block";
        }
    };
    // On clicking submit do following
    // $("button[type=submit]").click(function() {

    //     var atLeastOneChecked = false;
    //     $("input[type=radio]").each(function() {

    //         // If radio button not checked
    //         // display alert message 
    //         if ($(this).attr("checked") != "checked") {

    //             // Alert message by displaying
    //             // error message
    //             $("#msg").html(
    //                 "<span class='alert alert-danger' id='error'>" +
    //                 "Please Choose atleast one</span>");
    //         }
    //     });
    // });