$(document).ready(function () {
    // Function to load CSS file
    function loadCSS(href) {
        $("<link/>", {
            rel: "stylesheet",
            type: "text/css",
            href: href
        }).appendTo("head");
    }

    // Function to load external content
    function loadContent(contentPath) {
        $("#externalContent").load(contentPath);
    }

    // Event listener for clicking "Profile Details" under "Medical"
    $("#profile").on("click", function (e) {
        e.preventDefault(); // Prevent default link behavior
        // loadCSS($(this).data("css")); // Load CSS file
        loadContent($(this).data("content")); // Load external content
    });

    $("#med_tracker").on("click", function (e) {
        e.preventDefault(); // Prevent default link behavior
        loadContent("../../../templates/medical/medicalrequirements.html"); // Load external content
    });

    $("#emergency").on("click", function (e) {
        e.preventDefault(); // Prevent default link behavior
        loadContent("../../../templates/medical/profile.html"); // Load external content
    });

    $("#pwd").on("click", function (e) {
        e.preventDefault(); // Prevent default link behavior
        loadContent("../../../templates/medical/profile.html"); // Load external content
    });

    $("#dental").on("click", function (e) {
        e.preventDefault(); // Prevent default link behavior
        loadContent("../../../templates/medical/profile.html"); // Load external content
    });

    $("#med_cert").on("click", function (e) {
        e.preventDefault(); // Prevent default link behavior
        loadContent("../../../templates/medical/profile.html"); // Load external content
    });

    $("#pres").on("click", function (e) {
        e.preventDefault(); // Prevent default link behavior
        loadContent("../../../templates/medical/profile.html"); // Load external content
    });

    $("#trans").on("click", function (e) {
        e.preventDefault(); // Prevent default link behavior
        loadContent("../../../templates/medical/profile.html"); // Load external content
    });
});