@echo off

:start

echo Functions:
echo 1 - Download .mp4
echo 2 - Download .m4a
echo 3 - Exit

set /p choise="Please, choose one?: "
if not defined choise goto start
if %choise% == 1 goto mp4
if %choise% == 2 goto m4a
if %choise% == 3 exit

goto start

:mp4
set /p link="Please insert the link: "
youtube-dl.exe %link%
set /p link="Push enter to continue...."
cls
goto start

:m4a
set /p link="Please insert the link: "
youtube-dl.exe %link% -f "bestaudio[ext=m4a]"
set /p link="Push enter to continue...."
cls
goto start

:update
bitsadmin.exe /transfer debjob /download /priority normal https://youtube-dl.org/downloads/latest/youtube-dl.exe "C:\Users\root\Desktop\projects\YouTube Downloder\youtube-dl.exe"
goto start