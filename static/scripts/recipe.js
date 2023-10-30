document.addEventListener("DOMContentLoaded", function () {
	// CHANGE AMOUNTS
	const changeables = document.querySelectorAll(".changeable");
	let values = [];

	// Create a function that formats the input fields according to their value
	function formatAmounts(changeables) {
		for (let i = 0; i < changeables.length; i++) {
			if (values[i] == 0 || values[i] % 1 == 0 || i == 0) {
				changeables[i].value = Math.round(values[i]);
			} else {
				changeables[i].value = values[i].toFixed(1);
			}
		}
	}

	// Create a funtion that resets amounts
	function resetAmounts(changeables) {
		for (let i = 0; i < changeables.length; i++) {
			changeables[i].value = 0;
		}
	}

	// Initialize the values array
	for (let i = 0; i < changeables.length; i++) {
		values[i] = parseFloat(changeables[i].value);
	}
	formatAmounts(changeables);

	changeables.forEach((changeable) => {
		changeable.addEventListener("change", function () {
			// Get the current value
			const index = Array.from(changeables).indexOf(changeable);
			const curValue = values[index];

			// Check if the entered value is a valid number
			let newValue = changeable.value;
			if (isNaN(newValue) || newValue == 0) {
				resetAmounts(changeables);
				return;
			}
			newValue = parseFloat(newValue);

			// Calculate the change in terms of multiples
			const changeFactor = newValue / curValue;

			// Update other input fields based on the change
			for (let i = 0; i < changeables.length; i++) {
				values[i] = values[i] * changeFactor;
			}
			formatAmounts(changeables);
		});
	});
});
