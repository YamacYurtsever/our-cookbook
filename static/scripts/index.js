document.addEventListener("DOMContentLoaded", function () {
	recipeOpener();
	document.querySelector("#searchType").addEventListener("input", performSearch);
	document.querySelector("#searchQuery").addEventListener("input", performSearch);
});

// SEARCH
async function performSearch() {
	let type = document.querySelector("#searchType");
	let search = document.querySelector("#searchQuery");
	let query = await fetch("/?t=" + type.value + "&q=" + search.value);
	let responseText = await query.text();

	// Create a temporary div to parse the fetched HTML
	let tempDiv = document.createElement("div");
	tempDiv.innerHTML = responseText;

	// Extract the content of the "recipes" div
	let newRecipesContent = tempDiv.querySelector("#recipes").innerHTML;

	// Update the "recipes" div with the new content
	document.querySelector("#recipes").innerHTML = newRecipesContent;

	// Call the recipeOpener function after updating the content
	recipeOpener();
}

// Recipe Opener
function recipeOpener() {
	let recipes = document.querySelectorAll(".recipe");
	recipes.forEach(function (recipe) {
		recipe.addEventListener("click", function () {
			form = recipe.querySelector("form");
			form.submit();
		});
	});
}
