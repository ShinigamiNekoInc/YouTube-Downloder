i have a web server with php support, I need a web ui interface with dark theme, where I put a link on the video, then call it to the python scrypt "v3.0\python scrypts\download.py" (use it like a reference base code) on the backend server for download a video file, and return it to the user. all files put in folder "v3.0\web-service".

---

in project @/"v3.0\web-service - test" change folder from download to c:\temp

---

http://smartboxpc.local/projects/youtubedl/downloads/K%E2%A7%B8DA%20-%20FIRESTARTER%20ft.%20MIYEON%20and%20SOYEON%20of%20i-dle,%20Sophie%20Powers,%20Mimi%20Webb%20(Official%20Music%20Video).mkv

---

@/v3.0\web-service the const $pythonPath = 'C:\inetpub\libs\pythoncore-3.14-64\python.exe'; used in different files make in one pklace and global variable

---

i have functionality v3.0\web-service\php\cleanup.php to clean files, i need at the ui in section settings add block with label lioke "Download (206MB) or if it bigger count in GB" where we count size of the download folder and button to clean from folder