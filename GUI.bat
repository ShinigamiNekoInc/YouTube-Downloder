@echo off

:start

echo Functions:
echo 1 - Download .mp4
echo 2 - Download .m4a
echo 3 - Check update version
echo 4 - Exit

set /p choise="Please, choose one?: "
if not defined choise goto start
if %choise% == 1 goto mp4
if %choise% == 2 goto m4a
if %choise% == 3 goto update
if %choise% == 4 exit

goto start

:mp4
set /p link="Please insert the link: "
youtube-dl.exe %link% -f bestvideo,bestaudio
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
youtube-dl.exe -U
goto start