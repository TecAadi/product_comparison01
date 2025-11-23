from flask import Flask, render_template_string, request, redirect, jsonify, render_template
import os
from pymongo import MongoClient
from flask import Flask, render_template_string, request, redirect, session
from transformers import pipeline
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "static/uploads"  # Folder to save uploaded images

# Make sure the folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the image classifier once
classifier = pipeline("image-classification", model="google/vit-base-patch16-224")

app.secret_key = "aadi_super_secret_key_123"   # you can use any random string

# # Load the Transformer model ONCE
# classifier = load_transformer_model()
   

# -----------------------------------------------------
# 1) CONNECT TO MONGODB
# -----------------------------------------------------
Mongo_url = "mongodb+srv://honeycsk1414_db_user:9HbAzsHfRqzUavKs@apnaproject.vjc8brk.mongodb.net/"   # paste your real url
client = MongoClient(Mongo_url)

db = client["ecommerce_db"]         # database name
users_collection = db["users"]      # collection name



# -----------------------------------------------------
# 2) HOME PAGE UI  (Same as your original)
# -----------------------------------------------------
home_html = """
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>ProductComparison | Home</title>

  <style>
    body{
      font-family: Poppins, sans-serif;
      margin:0;
      padding:0;
      background:#f7f7f7;
      overflow-x:hidden;
      opacity:0;
      animation: fadeIn 1.2s ease forwards;
    }

    /* PAGE OPEN ANIMATION */
    @keyframes fadeIn {
      from { opacity:0; transform:scale(0.98); }
      to { opacity:1; transform:scale(1); }
    }

    /* PAGE EXIT ANIMATION */
    .page-exit {
      animation: pageClose 0.8s ease forwards;
    }

    @keyframes pageClose {
      from { opacity:1; transform:scale(1); }
      to { opacity:0; transform:scale(0.95); }
    }

    nav{
      background:#fff;
      padding:15px 30px;
      display:flex;
      justify-content:space-between;
      align-items:center;
      box-shadow:0 0 15px rgba(0,0,0,0.1);
      position:sticky;
      top:0;
      z-index:1000;
      transition:0.3s;
    }

    nav:hover {
      box-shadow:0 0 25px rgba(0,0,0,0.2);
      transform:translateY(-2px);
    }

    .links a{
      margin:0 14px;
      text-decoration:none;
      color:#555;
      font-weight:600;
      position:relative;
    }

    .links a::after {
      content:'';
      position:absolute;
      width:0%;
      height:3px;
      background:#007bff;
      left:0;
      bottom:-4px;
      transition:0.3s;
    }

    .links a:hover::after {
      width:100%;
    }

    .btn{
      padding:10px 20px;
      background:#007bff;
      color:#fff;
      border-radius:8px;
      border:none;
      cursor:pointer;
      transition:0.3s;
      font-size:15px;
    }

    .btn:hover {
      transform:scale(1.07);
      background:#0059d6;
    }

    .hero{
      padding:70px;
      text-align:center;
      background:linear-gradient(135deg,#87CEFA,#4682B4);
      color:white;
      animation: slideDown 1.4s ease;
    }

    @keyframes slideDown {
      from { transform: translateY(-70px); opacity:0; }
      to { transform: translateY(0); opacity:1; }
    }

    .hero h1{
      font-size:45px;
      margin-bottom:15px;
    }

    /* PRODUCT GRID */
    .grid{
      display:grid;
      grid-template-columns:repeat(auto-fit,minmax(250px,1fr));
      gap:25px;
      padding:50px;
    }

    .card{
      background:#fff;
      padding:20px;
      border-radius:15px;
      box-shadow:0 4px 15px rgba(0,0,0,0.1);
      transition:0.4s;
      opacity:0;
      transform: translateY(40px);
    }

    .card:hover {
      transform:translateY(-8px) scale(1.03);
      box-shadow:0 6px 20px rgba(0,0,0,0.2);
    }

    /* SCROLL ANIMATION */
    .show {
      opacity:1 !important;
      transform:translateY(0) !important;
      transition:0.8s ease;
    }

    footer{
      text-align:center;
      background:#111;
      color:#fff;
      padding:15px;
      margin-top:40px;
    }
  </style>

  <script>
    // PAGE EXIT ANIMATION
    function animateExit(url) {
      document.body.classList.add("page-exit");
      setTimeout(() => {
        window.location.href = url;
      }, 600);
    }

    // SCROLL ANIMATION
    window.addEventListener("scroll", function(){
      let elements = document.querySelectorAll(".card");
      elements.forEach(el => {
        let position = el.getBoundingClientRect().top;
        if (position < window.innerHeight - 50) {
          el.classList.add("show");
        }
      });
    });
  </script>

</head>

<body>

  <nav>
    <div style='font-size:26px;font-weight:bold;color:#007bff;cursor:pointer;' onclick="animateExit('/')">
      ProductComparison
    </div>

    <div class='links'>
      <a href="#" onclick="animateExit('/')">Home</a>
      <a href="#" onclick="animateExit('/about')">About</a>
      <a href="#" onclick="animateExit('/products')">Products</a>
      <a href="#" onclick="animateExit('/contact')">Contact</a>
    </div>

    <div>
      <button class='btn' onclick="animateExit('/login')">Login</button>
      <button class='btn' style='background:green' onclick="animateExit('/signup')">Sign Up</button>
    </div>
  </nav>

  <section class='hero'>
    <h1>Discover the Best Products</h1>
    <p>Your ultimate shopping destination with special offers.</p>
    <button class='btn'>Shop Now</button>
  </section>

  <section class='grid'>
    <div class='card'> <h3>Product 1</h3><p>Amazing quality product.</p><button class='btn'>Buy Now</button></div>
    <div class='card'> <h3>Product 2</h3><p>Limited time deal.</p><button class='btn'>Buy Now</button></div>
    <div class='card'> <h3>Product 3</h3><p>Best value item.</p><button class='btn'>Buy Now</button></div>
  </section>

  <footer>© 2025 ProductComparison. All Rights Reserved.</footer>

</body>
</html>
"""

# -----------------------------------------------------
# 3) LOGIN PAGE UI  (Same)
login_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Login | ShopEase</title>

<style>

    body {
        margin: 0;
        font-family: Poppins, sans-serif;
        background: linear-gradient(135deg, #6e8efb, #a777e3);
        height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        animation: fadeBg 1.2s ease-in-out;
    }

    @keyframes fadeBg {
        from {opacity: 0;}
        to {opacity: 1;}
    }

    .login-box {
        width: 350px;
        padding: 40px;
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        animation: popUp 0.7s ease;
    }

    @keyframes popUp {
        0% {transform: scale(0.5); opacity: 0;}
        100% {transform: scale(1); opacity: 1;}
    }

    .login-box h2 {
        text-align: center;
        margin-bottom: 30px;
        color: #fff;
        font-size: 28px;
        font-weight: 600;
    }

    .input-box {
        position: relative;
        margin-bottom: 25px;
    }

    .input-box input {
        width: 100%;
        padding: 12px 10px;
        background: rgba(255,255,255,0.2);
        border: none;
        outline: none;
        border-radius: 10px;
        color: #fff;
        font-size: 15px;
        transition: 0.3s;
    }

    .input-box input:focus {
        background: rgba(255,255,255,0.3);
        box-shadow: 0 0 10px rgba(255,255,255,0.5);
    }

    .login-btn {
        width: 100%;
        padding: 12px;
        background: #fff;
        color: #6e44ff;
        border: none;
        border-radius: 10px;
        cursor: pointer;
        font-size: 16px;
        font-weight: bold;
        transition: 0.3s;
    }

    .login-btn:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(255,255,255,0.4);
    }

    .signup-text {
        margin-top: 15px;
        text-align: center;
        color: white;
        font-size: 14px;
    }

    .signup-text a {
        color: yellow;
        font-weight: bold;
        text-decoration: none;
    }

    p {
        color: #ffdddd;
        text-align: center;
        margin-top: 10px;
    }

</style>
</head>

<body>

<div class="login-box">
    <h2>User Login</h2>
    
    <form method="POST">
        <div class="input-box">
            <input type="text" name="username" placeholder="Enter Username" required>
        </div>

        <div class="input-box">
            <input type="password" name="password" placeholder="Enter Password" required>
        </div>

        <button class="login-btn" type="submit">Login</button>
    </form>

    {% if error %}
    <p>{{ error }}</p>
    {% endif %}

    <div class="signup-text">
        Don't have an account? <a href="/signup">Sign Up</a>
    </div>

</div>

</body>
</html>
"""



# -----------------------------------------------------
# 4) SIGN UP PAGE UI  (Same)
# -----------------------------------------------------
signup_html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Create Account</title>

<style>
    body {
        margin: 0;
        padding: 0;
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        height: 100vh;
        font-family: "Poppins", sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: hidden;
    }

    /* Floating animation circles */
    .circle {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        animation: float 8s infinite ease-in-out;
    }

    .circle:nth-child(1) { width: 130px; height: 130px; top: 10%; left: 15%; animation-duration: 7s; }
    .circle:nth-child(2) { width: 200px; height: 200px; bottom: 10%; right: 10%; animation-duration: 9s; }
    .circle:nth-child(3) { width: 90px; height: 90px; top: 55%; left: 70%; animation-duration: 6s; }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-25px); }
        100% { transform: translateY(0px); }
    }

    .signup-box {
        width: 420px;
        background: rgba(255, 255, 255, 0.15);
        padding: 35px;
        border-radius: 15px;
        backdrop-filter: blur(12px);
        box-shadow: 0 0 30px rgba(0,0,0,0.2);
        z-index: 10;
        animation: fadeIn 0.9s ease-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .signup-box h2 {
        text-align: center;
        color: #fff;
        font-size: 30px;
        margin-bottom: 20px;
    }

    input {
        width: 100%;
        padding: 12px;
        margin: 8px 0;
        border-radius: 8px;
        border: none;
        outline: none;
        font-size: 15px;
    }

    button {
        width: 100%;
        padding: 12px;
        background: #00c6ff;
        border: none;
        color: white;
        font-size: 18px;
        border-radius: 8px;
        cursor: pointer;
        transition: 0.3s ease;
    }

    button:hover {
        background: #0072ff;
        transform: scale(1.02);
    }

    a button {
        margin-top: 15px;
        background: #4caf50;
    }

    p {
        text-align: center;
        color: white;
        font-size: 14px;
    }
</style>
</head>

<body>

<div class="circle"></div>
<div class="circle"></div>
<div class="circle"></div>

<div class="signup-box">
    <h2>Create Account</h2>

    <form method="POST">

        <input type="text" name="name" placeholder="Full Name" required>
        <input type="text" name="username" placeholder="Choose Username" required>
        <input type="password" name="password" placeholder="Choose Password" required>

        <input type="text" name="address" placeholder="Address" required>

        <label style="color:white">Date of Birth:</label>
        <input type="date" name="dob" required>

        <input type="text" name="city" placeholder="City" required>
        <input type="text" name="pincode" placeholder="Pincode" required>

        <button type="submit">Sign Up</button>
    </form>

    {% if error %}
    <p style="color: #ffdddd">{{ error }}</p>
    {% endif %}

    {% if success %}
    <p style="color: #c6ffdd">{{ success }}</p>
    {% endif %}

    <a href="/login"><button>Already have an account? Login</button></a>
</div>

</body>
</html>
"""

# -----------------------------------------------------
# 5) ROUTES (Updated to MongoDB)
# -----------------------------------------------------

@app.route("/")
def home():
    return render_template_string(home_html)


# ------------------ LOGIN BACKEND ---------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # FIND USER IN MONGODB
        user = users_collection.find_one({"username": username})

        if user and user["password"] == password:

                  # Store user session (important!)
               session["user"] = {
              "username": user["username"],
              "name": user["name"],
              "address": user["address"],
              "dob": user["dob"],
              "city": user["city"],
              "pincode": user["pincode"]
               }
               return redirect("/profile")

        else:
            error = "Invalid username or password"

    return render_template_string(login_html, error=error)


# ------------------ SIGN UP BACKEND -------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    success = None

    if request.method == "POST":
        uname = request.form["username"]

        # CHECK IF USER ALREADY EXISTS
        existing_user = users_collection.find_one({"username": uname})

        if existing_user:
            error = "Username already exists!"
        else:
            # INSERT NEW USER INTO MONGODB
            users_collection.insert_one({
                "name": request.form["name"],
                "username": uname,
                "password": request.form["password"],
                "address": request.form["address"],
                "dob": request.form["dob"],
                "city": request.form["city"],
                "pincode": request.form["pincode"]
            })

            success = "Account created successfully! Please login."

    return render_template_string(signup_html, error=error, success=success)


# Dummy Pages
@app.route("/about")
def about():
    return "<h1>About Page</h1>"

@app.route("/products")
def products():
    return "<h1>Products Page</h1>"

@app.route("/contact")
def contact():
    return "<h1>Contact Page</h1>"

profile_html = """
<<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Profile</title>

    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">

    <style>
        body {
            margin: 0;
            font-family: "Poppins", sans-serif;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            color: white;
            overflow-x: hidden;
            animation: fadeIn 1s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        /* Navbar */
        .navbar {
            width: 100%;
            padding: 15px 40px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            position: sticky;
            top: 0;
        }

        .navbar h2 {
            margin: 0;
            font-size: 26px;
            font-weight: 600;
        }

        .logout-btn {
            padding: 10px 20px;
            background: #ff4d4d;
            border: none;
            border-radius: 30px;
            color: white;
            font-size: 16px;
            cursor: pointer;
            transition: 0.3s;
        }

        .logout-btn:hover {
            background: #ff1a1a;
            transform: scale(1.05);
        }

        /* Profile Card */
        .profile-box {
            width: 450px;
            margin: 40px auto 0 auto;
            padding: 30px;
            background: rgba(255,255,255,0.15);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            text-align: center;
            animation: slideUp 0.8s ease-out forwards;
        }

        @keyframes slideUp {
            from { transform: translateY(40px); opacity: 0; }
            to   { transform: translateY(0px); opacity: 1; }
        }

        .profile-box img {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            border: 5px solid rgba(255,255,255,0.4);
            margin-bottom: 15px;
        }

        .info {
            text-align: left;
            margin-top: 25px;
        }

        .info p {
            background: rgba(255,255,255,0.15);
            padding: 12px;
            border-radius: 10px;
            margin-bottom: 12px;
        }

        /* Upload Section */
        .upload-box {
            width: 450px;
            margin: 40px auto 80px auto;
            padding: 25px;
            background: rgba(255,255,255,0.2);
            border-radius: 20px;
            backdrop-filter: blur(10px);
            text-align: center;
            animation: slideUp 0.8s ease-out forwards;
        }

        .upload-box input[type="file"] {
            margin-top: 15px;
        }

        .upload-btn {
            margin-top: 15px;
            padding: 10px 20px;
            background: #00eaff;
            border: none;
            border-radius: 30px;
            font-size: 16px;
            cursor: pointer;
            transition: 0.3s;
        }

        .upload-btn:hover {
            background: #00bcd4;
            transform: scale(1.05);
        }

        .prediction {
            margin-top: 20px;
            font-size: 18px;
            background: rgba(255,255,255,0.2);
            padding: 15px;
            border-radius: 12px;
        }

    </style>
</head>

<body>

    <!-- NAVBAR -->
    <div class="navbar">
        <h2>Welcome, {{ username }}</h2>
        <a href="/logout" style="text-decoration:none;">
            <button class="logout-btn">Logout</button>
        </a>
    </div>

    <!-- PROFILE BOX -->
    <div class="profile-box">
        <img src="https://cdn-icons-png.flaticon.com/512/149/149071.png">

        <h2>{{ username }}'s Profile</h2>

        <div class="info">
            <p><strong>Full Name:</strong> {{ name }}</p>
            <p><strong>User Name:</strong> {{ username }}</p>
            <p><strong>Address:</strong> {{ address }}</p>
            <p><strong>City:</strong> {{ city }}</p>
            <p><strong>DOB:</strong> {{ dob }}</p>
            <p><strong>Pincode:</strong> {{ pincode }}</p>
        </div>
    </div>

    <!-- UPLOAD + RECOGNIZE BOX -->
    <div class="upload-box">
        <h2>Upload Product Image</h2>

        <form action="/upload" method="POST" enctype="multipart/form-data">
            <input type="file" name="image" required>
            <br>
            <button class="upload-btn" type="submit">Recognize</button>
        </form>

        {% if result %}
            <div class="prediction">
                <strong>Prediction:</strong><br>
                {{ result[0].label }}  
                <br>
                <small>Score: {{ result[0].score }}</small>
            </div>
        {% endif %}
    </div>

</body>
</html>

"""

@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect("/login")

    user = session["user"]


    return render_template_string(
          profile_html,
          username=user["username"],
          name=user["name"],
          address=user["address"],
          city=user["city"],
          dob=user["dob"],
          pincode=user["pincode"]
        
      )
    

@app.route("/upload", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST":

        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]

        if file.filename == "":
            return "No selected file"

        # Save file
        filepath = os.path.join("static/uploads", file.filename)
        file.save(filepath)

        # Open and classify
        image = Image.open(filepath)
        result = classifier(image)

        return jsonify({"result": result})

    return render_template("upload.html")



# -----------------------------------------------------
# 6) RUN SERVER
# -----------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)


