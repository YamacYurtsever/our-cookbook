from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from datetime import datetime

from account import register_user, login_user, logout_user, login_required

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///project.db")

types = ["Sandwich", "Soup", "Pasta", "Pizza", "Salad", "Dessert", "Beverage", "Appetizer", "Fry",
         "Grill", "Snack", "Roast", "Stew", "Sauce", "Bread", "Rice", "Noodle", "Burger", "Taco", "Wrap", "Dip"]
cousines = ["Turkish", "Italian", "Chinese", "Indian", "Japanese", "Mexican", "French", "Thai",
            "Korean", "Spanish", "American", "Australian", "Albanian", "Portuguese", "Thai", "South American"]
measurements = ["count", "g", "ml", "cup", "tbsp", "tsp"]


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # OPEN RECIPE
        # Fetch recipe related info from the database
        recipeId = request.form.get("recipe-id")
        recipeDetails = db.execute(
            "SELECT username, title, type, cousine, image, weight, date, time FROM recipes JOIN users ON recipes.authorId = users.id WHERE recipeId = ?;", recipeId)
        recipeIngredients = db.execute(
            "SELECT amount, measurement, description FROM ingredients WHERE recipeId = ?;", recipeId)
        recipeSteps = db.execute(
            "SELECT number, description FROM steps WHERE recipeId = ? ORDER BY number;", recipeId)

        # Check if the user is the author of the recipe
        isAuthor = False
        authorId = db.execute(
            "SELECT authorId FROM recipes WHERE recipeId = ?;", recipeId)[0]["authorId"]
        try:
            if (authorId == session["user_id"]):
                isAuthor = True
        except:
            pass

        # Open the recipe page
        return render_template("recipe.html", recipeId=recipeId, recipeDetails=recipeDetails, recipeIngredients=recipeIngredients, recipeSteps=recipeSteps, isAuthor=isAuthor)

    else:
        # SEARCH
        type = request.args.get("t")
        query = request.args.get("q")
        if query:
            if type == "Recipe":
                recipes = db.execute(
                    "SELECT recipeId, username, title, type, cousine, image, date, time FROM recipes JOIN users ON recipes.authorId = users.id WHERE title LIKE ? ORDER BY date DESC, time DESC;", "%" + query + "%")
            else:
                recipes = db.execute(
                    "SELECT recipeId, username, title, type, cousine, image, date, time FROM recipes JOIN users ON recipes.authorId = users.id WHERE username LIKE ? ORDER BY date DESC, time DESC;", "%" + query + "%")
        else:
            recipes = db.execute(
                "SELECT recipeId, username, title, type, cousine, image, date, time FROM recipes JOIN users ON recipes.authorId = users.id ORDER BY date DESC, time DESC;")

        # Open the recipe page
        return render_template("index.html", recipes=recipes)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        # Recipe Details
        title = request.form.get("title")
        type = request.form.get("type")
        cousine = request.form.get("cousine")
        weight = request.form.get("weight")
        if not title or not weight:
            return render_template("error.html", error="Not All Necessary Fields Were Filled")
        if (type and type not in types) or (cousine and cousine not in cousines):
            return render_template("error.html", error="Wrong Input Format")
        try:
            weight = int(weight)
        except:
            return render_template("error.html", error="Wrong Input Format")
        title = title.lower().title()
        date = datetime.now().date()
        time = datetime.now().time()

        # Handle Image
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                # Generate a unique file name for the uploaded image using UUID
                import uuid
                unique_filename = str(uuid.uuid4()) + ".jpg"

                # Store it in the images directory
                image.save("static/images/" + unique_filename)
                image = "static/images/" + unique_filename
            else:
                image = "static/images/Default_Image.jpg"
        else:
            image = "static/images/Default_Image.jpg"

        # Ingredients
        ingredientAmounts = request.form.getlist("ingredientAmounts")
        ingredientMeasurements = request.form.getlist("ingredientMeasurements")
        ingredientDescriptions = request.form.getlist("ingredientDescriptions")
        for i in range(len(ingredientAmounts)):
            try:
                if not ingredientAmounts[i] or not ingredientMeasurements[i] or not ingredientDescriptions[i]:
                    return render_template("error.html", error="Not All Necessary Fields Were Filled")
            except:
                return render_template("error.html", error="Not All Necessary Fields Were Filled")
            ingredientDescriptions[i] = ingredientDescriptions[i].lower(
            ).title()
        try:
            float(ingredientAmounts[i])
        except ValueError:
            return render_template("error.html", error="Wrong Input Format")
        if ingredientMeasurements[i] not in measurements:
            return render_template("error.html", error="Wrong Input Format")

        # Steps
        stepDescriptions = request.form.getlist("stepDescriptions")
        stepNumbers = request.form.getlist("stepNumbers")
        for i in range(len(stepDescriptions)):
            if not stepDescriptions[i]:
                return render_template("error.html", error="Not All Necessary Fields Were Filled")
            stepDescriptions[i] = stepDescriptions[i].lower().title()

        # Add all to the database
        try:
            db.execute("INSERT INTO recipes (authorId, title, type, cousine, image, weight, date, time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       session["user_id"], title, type, cousine, image, weight, date, time)
            recipeId = db.execute("SELECT recipeId FROM recipes ORDER BY recipeId DESC")[
                0]["recipeId"]
            for i in range(len(ingredientAmounts)):
                db.execute("INSERT INTO ingredients (recipeId, amount, measurement, description) VALUES (?, ?, ?, ?)",
                           recipeId, ingredientAmounts[i], ingredientMeasurements[i], ingredientDescriptions[i])
            for i in range(len(stepDescriptions)):
                db.execute("INSERT INTO steps (recipeId, description, number) VALUES (?, ?, ?)",
                           recipeId, stepDescriptions[i], stepNumbers[i])
        except:
            return render_template("error.html", error="Couldn't Insert Into Database")

        return redirect("/")

    else:
        # Open add page
        return render_template("add.html", types=sorted(types), cousines=sorted(cousines), measurements=measurements)


@app.route("/delete")
@login_required
def delete():
    # Check if the user manually changed recipe Id
    recipeId = request.args.get("recipeId")
    ownerId = db.execute(
        "SELECT id from users JOIN recipes ON users.id = recipes.authorId WHERE recipeId = ?", recipeId)[0]["id"]
    if not ownerId == session["user_id"]:
        return render_template("error.html", error="You are not the owner")

    # Delte from database
    db.execute("DELETE FROM steps WHERE recipeId = ?;", recipeId)
    db.execute("DELETE FROM ingredients WHERE recipeId = ?;", recipeId)
    db.execute("DELETE FROM recipes WHERE recipeId = ?;", recipeId)

    return redirect("/")


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if request.method == "POST":
        # Check if the user manually changed recipe Id
        recipeId = request.form.get("recipeId")
        ownerId = db.execute(
            "SELECT id from users JOIN recipes ON users.id = recipes.authorId WHERE recipeId = ?", recipeId)[0]["id"]
        if not ownerId == session["user_id"]:
            return render_template("error.html", error="You are not the owner")

        # Recipe Details
        title = request.form.get("title")
        type = request.form.get("type")
        cousine = request.form.get("cousine")
        weight = request.form.get("weight")
        if not title or not weight:
            return render_template("error.html", error="Not All Necessary Fields Were Filled")
        if (type and type not in types) or (cousine and cousine not in cousines):
            return render_template("error.html", error="Wrong Input Format")
        try:
            weight = int(weight)
        except:
            return render_template("error.html", error="Wrong Input Format")
        title = title.lower().title()
        date = datetime.now().date()
        time = datetime.now().time()

        # Handle Image
        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                # Generate a unique file name for the uploaded image using UUID
                import uuid
                unique_filename = str(uuid.uuid4()) + ".jpg"

                # Store it in the images directory
                image.save("static/images/" + unique_filename)
                image = "static/images/" + unique_filename
            else:
                image = db.execute("SELECT image FROM recipes WHERE recipeId = ?;", recipeId)[
                    0]["image"]
        else:
            image = db.execute("SELECT image FROM recipes WHERE recipeId = ?;", recipeId)[
                0]["image"]

        # Ingredients
        ingredientAmounts = request.form.getlist("ingredientAmounts")
        ingredientMeasurements = request.form.getlist("ingredientMeasurements")
        ingredientDescriptions = request.form.getlist("ingredientDescriptions")
        for i in range(len(ingredientAmounts)):
            if not ingredientAmounts[i] or not ingredientMeasurements[i] or not ingredientDescriptions[i]:
                return render_template("error.html", error="Not All Necessary Fields Were Filled")
            ingredientDescriptions[i] = ingredientDescriptions[i].lower(
            ).title()
        try:
            float(ingredientAmounts[i])
        except ValueError:
            return render_template("error.html", error="Wrong Input Format")
        if ingredientMeasurements[i] not in measurements:
            return render_template("error.html", error="Wrong Input Format")

        # Steps
        stepDescriptions = request.form.getlist("stepDescriptions")
        stepNumbers = request.form.getlist("stepNumbers")
        for i in range(len(stepDescriptions)):
            if not stepDescriptions[i]:
                return render_template("error.html", error="Not All Necessary Fields Were Filled")
            stepDescriptions[i] = stepDescriptions[i].lower().title()

        # Add all to the database
        try:
            db.execute("UPDATE recipes SET title = ?, type = ?, cousine = ?, image = ?, weight = ?, date = ?, time = ? WHERE recipeId = ?",
                       title, type, cousine, image, weight, date, time, recipeId)
            db.execute("DELETE FROM ingredients WHERE recipeId = ?", recipeId)
            for i in range(len(ingredientAmounts)):
                db.execute("INSERT INTO ingredients (recipeId, amount, measurement, description) VALUES (?, ?, ?, ?)",
                           recipeId, ingredientAmounts[i], ingredientMeasurements[i], ingredientDescriptions[i])
            db.execute("DELETE FROM steps WHERE recipeId = ?", recipeId)
            for i in range(len(stepDescriptions)):
                db.execute("INSERT INTO steps (recipeId, description, number) VALUES (?, ?, ?)",
                           recipeId, stepDescriptions[i], stepNumbers[i])
        except:
            return render_template("error.html", error="Couldn't Insert Into Database")

        return redirect("/")

    else:
        # Check if the user manually changed recipe Id
        recipeId = request.args.get("recipeId")
        ownerId = db.execute(
            "SELECT id from users JOIN recipes ON users.id = recipes.authorId WHERE recipeId = ?", recipeId)[0]["id"]
        if not ownerId == session["user_id"]:
            return render_template("error.html", error="You are not the owner")

        recipeDetails = db.execute(
            "SELECT title, type, cousine, weight FROM recipes WHERE recipeId = ?;", recipeId)
        recipeIngredients = db.execute(
            "SELECT amount, measurement, description FROM ingredients WHERE recipeId = ?;", recipeId)
        recipeSteps = db.execute(
            "SELECT number, description FROM steps WHERE recipeId = ? ORDER BY number;", recipeId)

        return render_template("edit.html", types=types, cousines=cousines, measurements=measurements, recipeDetails=recipeDetails, recipeIngredients=recipeIngredients, recipeSteps=recipeSteps, recipeId=recipeId)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        return register_user()
    else:
        return render_template("register.html")


@app.route("/logout")
def logout():
    return logout_user()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        return login_user()
    else:
        return render_template("login.html")
