import cv2
import numpy as np
import face_recognition as fr
import os



# Función para encontrar la codificación de las imágenes.
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


# Función para marcar la asistencia.
def markAttendance(name):
    with open("Attendance.csv", "r+") as f:
        myDataList = f.readlines()
        nameList = []

        # Recorra la lista de datos y agregue los nombres a la lista de nombres
        for line in myDataList:
            entry = line.split(",")
            nameList.append(entry[0])

        # Si el nombre no está en la lista de nombres, agregue el nombre a la lista.
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime("%H:%M:%S")
            f.writelines(f"\n{name},{dtString}")


# Función para encontrar la cara.
def findFace(img):
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Encuentra las ubicaciones de las caras
    facesCurFrame = fr.face_locations(imgS)
    encodesCurFrame = fr.face_encodings(imgS, facesCurFrame)

    # Recorre las ubicaciones y codificaciones de las caras.
    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = fr.compare_faces(encodeListKnown, encodeFace)
        faceDis = fr.face_distance(encodeListKnown, encodeFace)

        # Encuentra el índice de la distancia mínima.
        matchIndex = np.argmin(faceDis)

        # Si la cara coincide entonces marca la asistencia.
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            print(name)

            # Dibuja el rectángulo alrededor de la cara.
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

            # Dibuja el rectángulo alrededor de la cara.
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Dibuja el rectángulo alrededor de la cara.
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)

            # Mostrar el codigo de la persona
            cv2.putText(
                img,
                name,
                (x1 + 6, y2 - 6),
                cv2.FONT_HERSHEY_COMPLEX,
                1,
                (255, 255, 255),
                2,
            )


# Cargue el img desde el directorio de la base de datos.
path = "database"
images = []
classNames = []
myList = os.listdir(path)

# Recorre las imágenes y agrégalas a la lista.
for cl in myList:
    curImg = cv2.imread(f"{path}/{cl}")
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

# Llame a la función para encontrar las codificaciones de las imágenes.
encodeListKnown = findEncodings(images)

# Iniciar la cámara web
cap = cv2.VideoCapture(0)

# Recorrer la cámara web
while True:
    success, img = cap.read()

    # Llame a la función para encontrar la cara.
    findFace(img)

    # Mostrar la imagen
    cv2.imshow("Webcam", img)

    # Si se presiona la tecla q, entonces se rompe el bucle.
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Suelta la cámara web
cap.release()

# Destruye todas las ventanas
cv2.destroyAllWindows()


print("its working dependencies")
