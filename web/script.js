var initialMouse = 0;
var slideMovementTotal = 0;
var mouseIsDown = false;
var slider = $('#slider');

slider.on('mousedown touchstart', function(event){
	mouseIsDown = true;
	slideMovementTotal = $('#button-background').width() - $(this).width() + 10;
	initialMouse = event.clientX || event.originalEvent.touches[0].pageX;
});

$(document.body, '#slider').on('mouseup touchend', function(event) {
    if (!mouseIsDown)
        return;
    mouseIsDown = false;
    var currentMouse = event.clientX || event.changedTouches[0].pageX;
    var relativeMouse = currentMouse - initialMouse;

    if (relativeMouse < slideMovementTotal) {
        $('.slide-text').fadeTo(300, 1);
        slider.animate({
            left: "-10px"
        }, 300);
        return;
    }
    // ON DRAG FUNCTIONALITY post request to the server
    var urlText = $('#gitUrl').val();
	console.log(urlText) // Assuming your input field has id "url-input"
    $.post('http://localhost:8000/description', {
        urlText: urlText
    }, function(data) {
        // Handle the response here and put it in the big-textarea-raw textarea
		$('#big-textarea-raw').val(data);
		$('#big-textarea-edited').val(data);
    });
});



$(document.body).on('mousemove touchmove', function(event){
	if (!mouseIsDown)
		return;

	var currentMouse = event.clientX || event.originalEvent.touches[0].pageX;
	var relativeMouse = currentMouse - initialMouse;
	var slidePercent = 1 - (relativeMouse / slideMovementTotal);
	
	$('.slide-text').fadeTo(0, slidePercent);

	if (relativeMouse <= 0) {
		slider.css({'left': '-10px'});
		return;
	}
	if (relativeMouse >= slideMovementTotal + 10) {
		slider.css({'left': slideMovementTotal + 'px'});
		return;
	}
	slider.css({'left': relativeMouse - 10});
});

document.addEventListener("DOMContentLoaded", function() {
    // Code inside this function will execute after the HTML is fully loaded
    setTimeout(function() {
        // Show the button
        var button = document.getElementById("proceed-button");
        if (button) {
            button.style.display = "block";
        }
    }, 3000); // Change 3000 to the time your loading takes in milliseconds
});
