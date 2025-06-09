import cv2
import numpy as np
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
cap = cv2.VideoCapture(0)
samples = []
labels = []
id_to_name = {}
user_count = int(input("👤 Nhap so nguoi can thu thap du lieu: "))
for i in range(user_count):
    user_id = i + 1
    name = input(f"📝 Nhap ten nguoi dung {user_id}: ")
    id_to_name[user_id] = name

    print(f"📸 Bat dau thu thap khuon mat cho {name}. Nhin vao webcam...")
    sample_count = 0
    target_samples = 30

    while sample_count < target_samples:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            roi = gray[y:y+h, x:x+w]
            samples.append(roi)
            labels.append(user_id)
            sample_count += 1

            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"{name} {sample_count}/{target_samples}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

        cv2.imshow("Thu thap du lieu", frame)
        if cv2.waitKey(1) == 27:
            break
print("✅ Huan luyen mo hinh...")
recognizer.train(samples, np.array(labels))
print("✅ San sang nhan dien!")
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
        if confidence < 100:
            name = id_to_name.get(id, "Khong ro")
            label = f"{name} ({100-int(confidence)}%)"
        else:
            label = "ERROR"
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.imshow("Nhan dien khuon mat", frame)
    if cv2.waitKey(1) == 27:
        break
cap.release()
cv2.destroyAllWindows()
