# Recipe Web Application

#### Video Demo: <https://www.youtube.com/watch?v=idmLhJUQ-2w&ab_channel=Yama%C3%A7Yurtsever>

#### Description:

This project is a web application built using Flask. The application allows users to create, view, edit, and delete recipes. Users can search for recipes based on the recipe and author names.

The project consists of the following main python files to handle back-end operations:

- `app.py`: The main Flask application file that contains all the routing and logic for handling requests related to recipes, search, adding, editing, and deleting recipes, as well as user authentication.

- `account.py`: A module containing functions for user registration, login, and logout.

The project utilizes a SQLite database (`project.db`) to store recipe and user information. It follows a structured approach to store recipe details, ingredients, and steps.

As well as these javascript files handiling front-end logic:

- `layout.js`: JavaScript file handling navbar highlighting for the selected page.

- `index.js`: JavaScript file handling the search functionality and recipe opening.

- `recipe.js`: JavaScript file handling the dynamic formatting of ingredient amounts.

- `add.js`: JavaScript file handling the addition and manipulation of rows in the recipe form for steps and ingredients.

The page templates consist of:

- `layout.html`, `index.html`, `recipe.html`, `register.html`, `login.html`, `add.html`, `edit.html`, `error.html`

The style sheets consist of:

- `layout.css`, `index.css`, `recipe.css`, `register-login.css`, `add.css`, `error.css`,

### Features

- **Recipe Search**: Users can search for recipes based on the recipe and author names.

- **Recipe Addition and Editing**: Authenticated users can add new recipes or edit (their own) existing ones, providing details such as title, type, cuisine, weight, image, ingredients, and steps.

- **Recipe Deletion**: Authenticated users can delete their own recipes.

- **Dynamic Ingredient Amounts**: Users can dynamically change ingredient amounts (e.g., in grams) while viewing a recipe, and all related materials (measurements, proportions, etc.) update accordingly on the frontend for a responsive and interactive user experience.

- **User Authentication**: Users can register, login, and logout.

### Design Choices

- **Database**: SQLite was chosen for its simplicity and ease of integration with Flask, making it suitable for this project.

- **Image Handling**: Uploaded images are saved in the `static/images/` directory with a unique filename generated using UUID to prevent naming conflicts.

- **Security**: Passwords are securely hashed using Werkzeug's `generate_password_hash` and checked using `check_password_hash`.

- **Input Validation**: Various input validations are implemented to ensure data integrity and prevent errors due to incorrect input formats.

### Potential Features

- **Common Features**: 
    - Search Filter: type, cousine, ingredients
    - Ratings, reviews, comments
    - Saving recipes

- **Using Public APIs**:
    - *Prices*: Using public APIs of scraped supermarket data, the app can automatically estimate the price of each recipe
    - *Nutrition*: An API can be used to fetch the nutritional values and calories of the ingredients in the recipes

- **My Fridge**: 
    - There could be page where the user enters the food items in their fridge and the app automatically shows the user all of the recipes in the database that they can make with the ingredients that they have
    - Using this, when the user views a recipe, the app can also show all of the necessary ingredients that the user doesn't already have
    - *Shopping List*: The user can add multiple recipes to their meal and the app generates a shopping list for the recipes, excluding the ingredients already in the fridge

- **Gamify**: 
    - Rating system can be utilized to have rankings of top users and a chef of the week

- **TikTok??**: 
    - The idea is that food content is really big on all social media 
platforms but there are no apps that focus on short form food content
    - The app could have a twitter like feed where each new recipe added is shown and the users can follow other users and have a personal feed of the people that they follow.