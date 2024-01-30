function select_thumbnail_button_clicked(thumbnail_button)
{ 
   document.getElementById("selected-usb-file-button").setAttribute("value", thumbnail_button.name);
   document.getElementById("selected-usb-file-button").click();
}