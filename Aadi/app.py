import os
return redirect(url_for("signup"))


hashed = generate_password_hash(request.form.get("password"))
users_collection.insert_one({
"name": request.form.get("name"),
"username": username,
"password": hashed,
"address": request.form.get("address"),
"dob": request.form.get("dob"),
"city": request.form.get("city"),
"pincode": request.form.get("pincode")
})
flash("Account created. Please login.", "success")
return redirect(url_for("login"))


return render_template("signup.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
if request.method == "POST":
username = request.form.get("username").strip()
password = request.form.get("password")
user = users_collection.find_one({"username": username})
if user and check_password_hash(user["password"], password):
session["user"] = {"_id": str(user.get("_id")), "username": user.get("username"), "name": user.get("name")}
flash("Logged in successfully", "success")
return redirect(url_for("home"))
else:
flash("Invalid username or password", "error")


return render_template("login.html")


# Logout
@app.route("/logout")
def logout():
session.pop("user", None)
flash("You have been logged out", "success")
return redirect(url_for("home"))


# Simple API to add demo products (for dev only)
@app.route("/admin/add-demo-products")
def add_demo_products():
demo = [
{"title": "Wireless Headphones", "price": "1999", "desc": "Great sound"},
{"title": "Smart Watch", "price": "4999", "desc": "Track fitness"},
{"title": "Gaming Mouse", "price": "1299", "desc": "High DPI"}
]
products_collection.insert_many(demo)
return "Added demo products"


if __name__ == '__main__':
# For development only. In production use gunicorn and set debug=False
app.run(debug=True, port=int(os.getenv("PORT", 5000)))