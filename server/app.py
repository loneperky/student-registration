from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from config import MONGO_URL

app = Flask(__name__)

CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173"],  # Your frontend URL
        "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    },
    r"/*": {  # Global fallback (optional but recommended)
        "origins": ["http://localhost:5173"],
        "methods": ["GET", "POST", "OPTIONS"]
    }
})


# set up MongoDB connection
client = MongoClient(MONGO_URL)
db = client["user_database"]
students = db["students"]


@app.route("/")
def test():
    return jsonify({"status": "API is running", "endpoints": {
        "/api/register": "POST",
        "/search/<matno>": "GET",
        "/all/students": "GET"
    }})

# routes to handle requests
@app.route("/api/register", methods=["POST","OPTIONS"])
def register_student():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
        response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    data = request.get_json()
    fullname = data.get("fullname")
    age = data.get("age")
    matno = data.get("matno")
    gender = data.get("gender")
    dept = data.get("dept")
    level = data.get("level")
    faculty = data.get("faculty")
    skills = data.get("skills")
    
    if not fullname or not age or not matno or not dept or not level or not faculty:
      return jsonify({"error": "All fields are required"}), 400
      
    existing = students.find_one({"matno":matno})
    if existing:
      return jsonify({"error":"User already exist"})
    
    single_student = {
      "fullname":fullname,
      "age":age,
      "matno":matno,
      "gender":gender,
      "dept":dept,
      "level":level,
      "faculty":faculty,
      "skills":skills
    }
    students.insert_one(single_student)
    return jsonify({"message": "User registered successfully", "data": data}), 201
  

# Route to search student using matno
@app.route("/search/<matno>", methods = ["GET"])
def single_student(matno):
  student = students.find_one({"matno":matno},{"_id":0})
  if student:
    return jsonify(student),200
  else:
    return jsonify({"error":"Student not found"})


# Route to get all students
@app.route("/all/students", methods = ["GET"])
def get_all_students():
  all_students =list(students.find({},{"_id":0})) 
  if all_students:
    return jsonify(all_students)
  else:
    return jsonify({"error":"Error fetching students"})


  
if __name__ == "__main__":
  app.run(host="localhost", port=7000, debug=True)
  