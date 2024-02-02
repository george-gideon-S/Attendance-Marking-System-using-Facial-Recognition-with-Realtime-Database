# import necessary modules
import os
import cv2
import pickle
import numpy as np
import face_recognition
from datetime import datetime
# import database modules
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage



### Initializing the requirements for marking attendance.
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-attendance-realtime-56b4cd-default-rtdb.firebaseio.com/",
    "storageBucket": "face-attendance-realtime-56b4cd.appspot.com"
})

bucket = storage.bucket()


# Set the camera to the webcam
cap = cv2.VideoCapture(0)
# Set the dimensions
cap.set(3,640)
cap.set(4,480)


# Get the background image
imgBackground = cv2.imread("Resources/background.png")


### importing the Mode Images to imgModeList
folderModePath = "Resources/Modes"
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))


### Load the Encode File i.e EncodeFile.p
print("Loading Encode file...")         # START
file = open("EncodeFile.p", 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
print("Encode File loaded!!!")          # STOP

# ALready existing encodings are loaded 
encodeListKnown, studentIds = encodeListKnownWithIds
print(studentIds)
# print(encodeListKnown)


modeType = 0
counter = 0
id_ = -1
imgStudent = []


while True:
    # captures image
    success, img = cap.read()

    # resize the image "img"
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    # Convert the resized image from BGR to RGB since face_recognition requires RGB
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)


    ### The sole purpose is to compare the CURRENT encodings with already EXISTING encodings.
    # get the location of the face (no need to consider the whole face)
    faceCurrFrame = face_recognition.face_locations(imgS)
    # find the encodings of captured image/person - CURRENT encodings
    encodeCurrFrame = face_recognition.face_encodings(imgS, faceCurrFrame)

    # positioning captured image inside imgBackground
    imgBackground[162:162+480, 55:55+640] = img
    imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]


    if faceCurrFrame:
        ### Compare the PREVIOUSLY EXISTED encodings with CURRENT Encodings
        for encodeFace, faceLoc in zip(encodeCurrFrame, faceCurrFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print(f"Face matched or not [yes/no]: {matches}")
            print(f"Distance b/w known & current face: {faceDis}")      # distance with min magnitude is the right match


            # extract the index of least value
            matchIndex = np.argmin(faceDis)
            # print(f"Match Index: {matchIndex}")


            # check if the right face was detected
            if matches[matchIndex]:
                print(f"Student Id: {studentIds[matchIndex]}. Known face detected!!!")

                # Create a rectangle around the face
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4     # since we've reduced by 1/4th
                bbox = 55+x1, 162+y1, x2-x1, y2-y1
                imgBackground = cv2.rectangle(imgBackground, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 255, 0), 2)
                # imgBackground = cv2.rectangle(imgBackground, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)

                # Create a rectangle around the face
                # y1, x2, y2, x1 = faceLoc
                # y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4     # since we've reduced by 1/4th
                # bbox = 55+x1, 162+y1, x2-x1, y2-y1
                # imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

                # matched index
                id_ = studentIds[matchIndex]
                print(id_)

                if counter == 0:
                    # cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.putText(imgBackground, "Loading", (275, 400), cv2.FONT_HERSHEY_COMPLEX, 1, (51, 255, 153), 1)
                    cv2.imshow("Background Image", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter!= 0:
            if counter == 1:
                # get the data
                studentInfo = db.reference(f"Students/{id_}").get()
                print(studentInfo)

                # get the image from the storage
                blob = bucket.get_blob(f"Images/{id_}.jpg")
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

                # update the data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(f"Seconds Elapsed: {secondsElapsed}")


                # waits for 30 seconds to mark attendance again
                if secondsElapsed > 5:
                    ref = db.reference(f"Students/{id_}")
                    studentInfo["total_attendance"] += 1
                    ref.child("total_attendance").set(studentInfo["total_attendance"])
                    ref.child("last_attendance_time").set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]


            if modeType != 3:

                if 10<counter<20:
                    modeType = 2
                imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]

                if counter <= 10:
                    # set the coordinates except for name
                    cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 1)
                    cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)
                    cv2.putText(imgBackground, str(id_), (1006, 493), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)
                    cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)
                    cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)
                    cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625), cv2.FONT_HERSHEY_COMPLEX, 0.6, (100,100,100), 1)

                    # positioning the coordinates for name
                    (w, h), _ =  cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (414-w)//2
                    cv2.putText(imgBackground, str(studentInfo['name']), (808+offset, 445), cv2.FONT_HERSHEY_COMPLEX, 1, (50,50,50), 1)



                    # imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

                    # Assuming you want to resize imgStudent to (216, 216)
                    imgStudent = cv2.resize(imgStudent, (216, 216))

                    # Assign the resized imgStudent to the specified region in imgBackground
                    imgBackground[175:175 + 216, 909:909 + 216] = imgStudent


                counter+=1


                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[44:44+633, 808:808+414] = imgModeList[modeType]

    else:
        modeType = 0
        counter = 0

    cv2.imshow("Background Image", imgBackground)
    cv2.waitKey(1)