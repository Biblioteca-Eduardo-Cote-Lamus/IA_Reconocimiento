
import cv2
import numpy as np
import face_recognition as fr
import os

# solo para tomar fotos en collan
from IPython.display import display, Javascript, Image
from google.colab.output import eval_js
from base64 import b64decode

class IAReconocimiento():

  def take_photo(self, filename='photo.jpg', quality=0.8):
    js = Javascript('''
      async function takePhoto(quality) {
        const div = document.createElement('div');
        const capture = document.createElement('button');
        capture.textContent = 'Capture';
        div.appendChild(capture);

        const video = document.createElement('video');
        video.style.display = 'block';
        const stream = await navigator.mediaDevices.getUserMedia({video: true});

        document.body.appendChild(div);
        div.appendChild(video);
        video.srcObject = stream;
        await video.play();

        // Resize the output to fit the video element.
        google.colab.output.setIframeHeight(document.documentElement.scrollHeight, true);

        // Wait for Capture to be clicked.
        await new Promise((resolve) => capture.onclick = resolve);

        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        stream.getVideoTracks()[0].stop();
        div.remove();
        return canvas.toDataURL('image/jpeg', quality);
      }
      ''')
    display(js)
    data = eval_js('takePhoto({})'.format(quality))
    binary = b64decode(data.split(',')[1])
    with open(f'{filename}', 'wb') as f:
      f.write(binary)
    # # Display the captured photo
    # display(Image(data=binary))
    return f'{filename}'

  # Función para encontrar la codificación de las imágenes.
  def findEncodings(self,images):
      encodeList = []
      for img in images:
          img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
          encode = fr.face_encodings(img)[0]
          encodeList.append(encode)
      return encodeList

  
  def recognition(self):
    # Cargue el img desde el directorio de la base de datos.
    path = "database"
    images = []
    classNames = []
    myList = os.listdir(path)

    # Recorre las imágenes y agrégalas a la lista.
    for cl in myList:
        # print(cl)
        curImg = cv2.imread(f"{path}/{cl}")
        images.append(curImg)
        classNames.append(os.path.splitext(cl)[0])

    # Llame a la función para encontrar las codificaciones de las imágenes.
    encodeListKnown = self.findEncodings(images)
    filename = self.take_photo()
    img = cv2.imread(filename)
    print(self.findFace(img ,encodeListKnown, classNames))


# Función para encontrar la cara.
  def findFace(self,img, encodeListKnown,classNames):
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

          # Verifica si la coincidencia es mayor o igual al 95%
          if matches[matchIndex] and faceDis[matchIndex] < 0.95:
              name = classNames[matchIndex].upper()
          else:
              name = "Desconocido"

          return name
