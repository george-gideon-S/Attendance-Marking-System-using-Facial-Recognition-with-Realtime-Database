import os
import cv2
import pickle
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage


### Initializing the requirements for sending images to Storage.
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-attendance-realtime-56b4cd-default-rtdb.firebaseio.com/",
    "storageBucket": "face-attendance-realtime-56b4cd.appspot.com"
})


## importing the Student Images to imgStudentList
folderPath = "Images"
PathList = os.listdir(folderPath)
imgStudentList = []
studentIds = []
for path in PathList:
    imgStudentList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])        # Extracting ids from Student Images [removing extension]

    fileName = f"{folderPath}/{path}"
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)


# Function to get the Encodings of Student Images
def findEncodings(imagesList):
    encodeList = []     # Encodings of all Student Images
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)      # Since Face Recognition only accepts RGB.
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList   # Returns the Encodings

# Get the Encodings of Student Images
print("Encoding Began...")
encodeListKnown = findEncodings(imgStudentList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Done!!!")


# Dump the data into a pickle file
file = open("EncodeFile.p", "wb")
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("Data dumped into the pickle file!!!")