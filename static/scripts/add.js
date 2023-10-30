document.addEventListener("DOMContentLoaded", function () {
	reorderRows();
});

function reorderRows() {
	let grids = document.querySelectorAll(".grid");
	grids.forEach((grid) => {
		let rows = grid.querySelectorAll(".row");
		rows.forEach((row) => {
			// If it is the steps grid, manage the move up button
			let numDiv = row.querySelector(".step-num");
			let numMemory = row.querySelector(".step-num-db");
			if (numDiv) {
				let num = parseInt(numDiv.innerHTML.slice(0, -1));
				row.style.order = num;
				numMemory.value = num;
				if (num > 1) {
					row.querySelector(".moveUpButton").removeAttribute("hidden");
				} else {
					row.querySelector(".moveUpButton").setAttribute("hidden", "hidden");
				}
			}

			// Center the rows
			if (rows.length > 1) {
				row.style.justifyContent = "flex-end";
			} else {
				row.style.justifyContent = "center";
			}
		});

		// If there is more than one row show the remove button
		if (grid.children.length > 1) {
			for (let i = 0; i < grid.children.length; i++) {
				const stepButton = grid.children[i].querySelector(".removeButton");
				stepButton.removeAttribute("hidden");
			}
		}
	});
}

function addRow(button) {
	const grid = button.previousElementSibling;
	let lastRow = grid.lastElementChild;
	let clonedRow = lastRow.cloneNode(true);

	// Increment the step number
	let numDiv = clonedRow.querySelector(".step-num");
	if (numDiv != null) {
		let num = parseInt(numDiv.innerHTML.slice(0, -1));
		num++;
		numDiv.innerHTML = num + ".";
	}

	// Clear the description
	let description = clonedRow.querySelector(".description");
	description.value = "";

	// Clear the amount
	let amount = clonedRow.querySelector(".ingredient-amount");
	if (amount !== null) {
		amount.value = "";
	}

	// Clear the measurement
	let measurement = clonedRow.querySelector(".ingredient-measurement");
	if (measurement !== null) {
		measurement.selectedIndex = 0;
	}

	// Add the new row
	grid.append(clonedRow);

	// Reorder Rows
	reorderRows();
}

function removeRow(button) {
	const row = button.parentElement;
	const grid = row.parentElement;

	// Remove the row
	row.remove();

	// Set the number of each row according to the new order
	for (let i = 0; i < grid.children.length; i++) {
		const existingRow = grid.children[i];
		const numDiv = existingRow.querySelector(".step-num");
		if (numDiv != null) {
			numDiv.innerHTML = i + 1 + ".";
		}
	}

	// If there is only one row left hide the remove button
	if (grid.childElementCount == 1) {
		grid.children[0].querySelector(".removeButton").setAttribute("hidden", "hidden");
	}

	// Reorder Rows
	reorderRows();
}

function moveUpRow(button) {
	// Get the current row
	let curRow = button.parentElement;
	let curRowStep = curRow.querySelector(".step-num");
	let curRowStepNum = parseInt(curRowStep.innerHTML.slice(0, -1));

	// Get the above row
	let rows = document.querySelectorAll(".row");
	let aboveRow;
	rows.forEach((row) => {
		let rowStep = row.querySelector(".step-num");
		if (rowStep) {
			let rowStepNum = parseInt(rowStep.innerHTML.slice(0, -1));
			if (rowStepNum == curRowStepNum - 1) {
				aboveRow = row;
				return;
			}
		}
	});
	let aboveRowStep = aboveRow.querySelector(".step-num");
	let aboveRowStepNum = parseInt(aboveRowStep.innerHTML.slice(0, -1));

	// Change the step nums of the two rows
	curRowStep.innerHTML = aboveRowStepNum + ".";
	aboveRowStep.innerHTML = curRowStepNum + ".";

	// Reorder Rows
	reorderRows();
}
