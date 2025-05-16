from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from config import MONGO_URL

app = Flask(__name__)

CORS(app, origins=["http://localhost:5173","https://student-registration-frontend.vercel.app","http://127.0.0.1:5173"])


# set up MongoDB connection
client = MongoClient(MONGO_URL)
db = client["user_database"]
students = db["students"]

# routes to handle requests
@app.route("/api/register", methods=["POST"])
def register_student():
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


# @app.after_request
# def apply_cors_headers(response):
#     response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
#     response.headers.add("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
#     return response
  
if __name__ == "__main__":
  app.run(debug=True)
  