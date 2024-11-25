Automatic Attendance System 🧑‍🏫

A Python-based attendance tracking system that uses facial recognition to monitor student attendance during scheduled classes.

---

🛠 Features
- Facial Recognition**: Detects and recognizes multiple faces in real-time using OpenCV.
- Class Schedule Integration**: Tracks attendance based on the provided timetable (`time_table.json`).
- Detailed Reports**: Saves attendance data to an Excel file, including time spent in class.

---

🚀 How to Use
1. Clone the repository and place face images for recognition in the `images` folder.
2. Add your class schedule in a `time_table.json` file.
3. Run the script:
   ```bash
   python attendance_system.py
4. The system will save the attendance as an Excel file after the class ends.
---

📋 Requirements
Python 3.7+
Libraries: OpenCV, Pandas, simple_facerec
Install dependencies using:
---

📁 File Structure
time_table.json: Class schedule in JSON format.
images/: Folder containing face images for recognition.
attendance_system.py: Main script for the attendance system.

bash
Copy code
