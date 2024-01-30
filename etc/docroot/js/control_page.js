var values = [1, 10, 50, 100];

jQuery('#move-z-slider').change(function() 
{
  document.getElementById('z-step').innerHTML = values[this.value] 
 
});