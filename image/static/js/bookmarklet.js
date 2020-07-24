(function(){
    var jquery_version = "3.4.1";
    var site_url = "https://127.0.0.1:8000/";
    var static_site = site_url + "static/";
    var min_width = 100;
    var max_height = 100;

    function bookmarklet(msg){
        // Here goes our bookmarklet code
        // Load CSS
        var css = jQuery("<link>");
        css.attr({
            rel : "stylesheet",
            type : "text/css",
            href : static_site + "css/bookmarklet.css?r=" + Math.floor(Math.random()*99999999999999999999)
        });
        jQuery("head").append(css);

        // Load HTML
        box_html = "<div id='bookmarklet'><a href='#' id='close'>&times;</a><h1>Select an image to bookmark:</h1><div class='images'></div></div>";
        jQuery("body").append(box_html);

        // Close event
        jQuery("#bookmarklet #close").click(function(){
            jQuery("#bookmarklet").remove();
        })

        // Find the images and display them
        jQuery.each(jQuery("img[src$='jpg']"), function(index, image){
            if (jQuery(image).width() >= min_width && jQuery(image).height() >= max_height){
                image_url = jQuery(image).attr("src");
                jQuery("#bookmarklet .images").append('<a href="#"><img src="'+image_url+'" /></a>');
            }
        })

        // Bookmark the selected image
        jQuery("#bookmarklet .images a").click(function(e){
            selected_image = jQuery(this).children("img").attr('src');
            // Hide the bookmarklet
            jQuery("#bookmarklet").hide();
            // Open new webdite to submit the image
            window.open(site_url+"images/create/?url="
                            + encodeURIComponent(selected_image)
                            + "&title="
                            + encodeURIComponent(jQuery("title").text()),
                            "_blank");

        });
    };

    // Check if the jQuery is loaded
    if(typeof window.jQuery != "undefined"){
        bookmarklet();
    } else {
        // Check for conflics
        var conflict = typeof window.$ != "undefined";
        // Create the script and points to Google API
        var script = document.createElement('script');
        script.src = "//ajax.googleapis.com/ajax/libs/jquery/" + jquery_version + "/jquery.min.js";
        // Add the script between the head tag
        document.head.appendChild(script);
        // Create a way to wait until script is loaded
        (function(){
            // Check if JQuery is loaded
            if (typeof window.jQuery == "undefined"){
              if (--attempts > 0){
                // Calls himself in a few milliseconds
                window.setTimeout(arguments.callee, 250);
              }
              else {
                // Too many attempts to load, send error
                alert("An error has occured while loading jQuery")
              }
            } else {
                bookmarklet();
            }
        });
    }
})();