import cv2
import pandas as pd
import json
from datetime import datetime, timedelta
from source_code.simple_facerec import SimpleFacerec

# Load timetable
with open('time_table.json', 'r') as file:
    timetable = json.load(file)

# Get current class
def get_current_class(day, current_time):
    day_schedule = timetable.get(day.lower(), {})
    for time_range, class_name in day_schedule.items():
        start_time, end_time = time_range.split('-')
        start_time = datetime.strptime(start_time, "%H:%M").time()
        end_time = datetime.strptime(end_time, "%H:%M").time()
        if start_time <= current_time <= end_time:
            return class_name, start_time, end_time
    return None, None, None

# Encode faces
sfr = SimpleFacerec()
sfr.load_encoding_images("E:/College Project/Face Detection Module/source_code/images")

# Load camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Initialize attendance tracking
attendance = {}
start_time = datetime.now()
current_day = datetime.now().strftime("%A")
current_class, class_start_time, class_end_time = get_current_class(current_day, start_time.time())

if current_class is None:
    print("No class scheduled for this time.")
    cap.release()
    exit()

class_duration = (datetime.combine(datetime.today(), class_end_time) - datetime.combine(datetime.today(), class_start_time)).seconds // 60

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Detect multiple faces
    face_locations, face_names = sfr.detect_known_faces(frame)

    # Track time for each student
    current_time = datetime.now()
    for name in face_names:
        if name not in attendance:
            attendance[name] = {
                "start_time": current_time.strftime("%H:%M:%S"),
                "end_time": None,
                "time_in_class": timedelta(),
                "last_seen": current_time
            }
        else:
            time_diff = current_time - attendance[name]["last_seen"]
            attendance[name]["time_in_class"] += time_diff
            attendance[name]["last_seen"] = current_time
            attendance[name]["end_time"] = current_time.strftime("%H:%M:%S")

    # Display the frame with rectangles for detected faces
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 200), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 200), 2)

    cv2.imshow("Frame", frame)

    if datetime.now() >= datetime.combine(datetime.today(), class_end_time) or cv2.waitKey(1) == 27:
        break

# Save attendance data
cap.release()
cv2.destroyAllWindows()

attendance_data = []
for student, data in attendance.items():
    time_spent_in_class = data["time_in_class"].total_seconds() / 60
    attendance_data.append([
        student,
        current_class,
        class_duration,
        data["start_time"],
        data["end_time"] or datetime.now().strftime("%H:%M:%S"),
        time_spent_in_class
    ])

# Save to Excel
df = pd.DataFrame(attendance_data, columns=["Student Name", "Class Name", "Class Duration (minutes)", "Start Time", "End Time", "Time in Class (minutes)"])
filename = f"{current_class}_attendance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
df.to_excel(filename, index=False)

print(f"Attendance saved to {filename}")
