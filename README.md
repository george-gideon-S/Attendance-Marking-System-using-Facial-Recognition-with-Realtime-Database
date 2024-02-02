# Attendance-Marking-System-with-Realtime-Database
This project is powered by OpenCV, designed to automate attendance through face detection. This repository includes the codebase for real-time face recognition, finding encodings and a database that dynamically updates attendance. Enhance your attendance management with this efficient and user-friendly solution.

## Project Steps

1. Webcam.
2. Graphics.
3. Encoding Generator.
4. Face Recognition.
5. Database Setup.
6. Add data to Database.
7. Add images to Database.
8. Realtime database update.
9. Limit attendance as per the day.

## Important Instructions

1. Download the Zip file in your current project folder and don't reorder.
2. Set the size of each image to 216x216 resolution.
3. Get the ServiceAccountKey.json from,
   * Go to Project Settings.
   * Go to Service Accounts.
   * Click on "Generate new private key".
4. Get the "databaseURL" (in code) from the link provided in "Realtime Database" of Firebase Database.
5. Get the "storageBucket" URL (in code) from the link provided in "Storage" of Firebase Database.

## Requirements

* Python 3.3+ or Python 2.7.

## Installation Guide

* First, make sure you have dlib already installed.

  ```
  pip install dlib
  ```
* Then, make sure you have cmake installed.

  ```
  pip install cmake
  ```
* Then, install C++ on your system (Visual Studio - C++ Web Development).
* Finally, install face_recognition module from pypi using `pip3` or `pip2` for Python 2.

  ```
  pip3 install face_recognition
  ```
* **Other Modules:** numpy, os, firebase_admin, pickle.

## Credits

#### Having problems?

If you run into problems, contact me on Twitter @itsgergesale.


#### Thanks

Many thanks to the originator of this project, Mr. Murtaza Hassan.

