document.getElementById("connect-hotspot-btn").onclick = function() {connect_hotspot()};
document.getElementById("connect-wifi-btn").onclick = function() {connect_wifi()}


function connect_hotspot() 
{
    document.getElementById("connect-hotspot-btn-hidden").click();     
}

function connect_wifi()
{
    document.getElementById("connect-wifi-btn-hidden").click();   
}