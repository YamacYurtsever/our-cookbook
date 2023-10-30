//NAVBAR HIGHLIGHT SELECTED PAGE
document.addEventListener("DOMContentLoaded", function () {
	let navElements = document.querySelectorAll("#navbar div *");
	let navObject = {};

	navElements.forEach(function (element) {
		if (element.innerHTML != "Our Cookbook") {
			if (element.innerHTML == "Home") {
				navText = "";
			} else if (element.innerHTML == "Add Recipe") {
				navText = "add";
			} else {
				navText = element.innerHTML.replace(/\s/g, "").toLowerCase();
			}
			navObject[navText] = element.parentElement;
		}
	});

	let path = window.location.pathname.split("/").pop();

	for (let key in navObject) {
		if (key === path) {
			navObject[key].style.backgroundColor = "darkgrey";
			navObject[key].style.border = "2px solid black";
		}
	}
});
