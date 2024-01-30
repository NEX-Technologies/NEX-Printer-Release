/*
    This script reads a text file located 
    at /files/web_print_status.txt, parses its
    key-value pair and sets the value attribute of:

    - printing-name
    - printing-current-layer
    - printing-remaining-time

    in the /printing.html

    It does this every 3 seconds to replicate a real time
    update of the print progress during printing.
*/

//alert("[DEBUG] web_print_status.js loaded.");

$(document).ready(function () 
{

    function functionToLoadFile() 
    {

        //alert("[DEBUG] web_print_status.js function call: functionToLoadFile()");

        
        jQuery.get('/files/web_print_status.txt?=' + + new Date().getTime(), function (data, status) {
            
            //alert("[DEBUG] web_print_status contents: " + data);
            
            // Parse contents of the data here.
            var data_split = data.split("\n");
            var printing_name = data_split[0].split("=")[1].trim();
            var printing_current_layer = data_split[1].split("=")[1].trim();
            var printing_remaining_time = data_split[2].split("=")[1].trim();
            var printing_percentage = data_split[3].split("=")[1].trim();
            var printing_current_image_path = data_split[4].split("=")[1].trim()

            // alert("printing_name: " + printing_name);
            // alert("printing_current_layer: " + printing_current_layer);
            // alert("printing_remaining_time: " + printing_remaining_time);
            // alert("printing_percentage: " + printing_percentage);
            // alert("printing_current_image_path: " + printing_current_image_path);
 
            // Load the progress bar.
            var ctx = document.getElementById('circularLoader').getContext('2d');
            var al = parseFloat(printing_percentage);
            var start = 4.72;
            var cw = ctx.canvas.width;
            var ch = ctx.canvas.height; 
            var diff;
         
            diff = ((al / 100) * Math.PI*2*10).toFixed(2);
            ctx.clearRect(0, 0, cw, ch);
            ctx.lineWidth = 17;
            ctx.fillStyle = '#4285f4';
            ctx.strokeStyle = "#4285f4";
            ctx.textAlign = "center";
            ctx.font="28px monospace";
            ctx.fillText(al+'%', cw*.52, ch*.5+5, cw+12);
            ctx.beginPath();
            ctx.arc(100, 100, 75, start, diff/10+start, false);
            ctx.stroke();


            // Change the value of the parametrs needed
            // in printing.html
            jQuery('#printing-name').attr("value", printing_name)
            jQuery('#printing-current-layer').attr("value", printing_current_layer)
            jQuery('#printing-remaining-time').attr("value", printing_remaining_time)
            // Progress percentage is in the circular bar itself.
            jQuery('#current-image-path').attr("src", printing_current_image_path +"?"+(new Date()).getTime())
             

            // Check the value of val, if it is 100,
            // we redirect back to /print and set it to 0.

            if(al== 100)
            {
                al = 0;
                window.location.replace("/print");
            }

        });

        // Call the function repeatedly every 1 second.
        setTimeout(functionToLoadFile, 1000);
    }

    
    // Call the function for the first time.
    setTimeout(functionToLoadFile, 1000);


});
