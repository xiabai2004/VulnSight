@echo off
echo protocol=https>%TEMP%\cred_input.txt
echo host=github.com>>%TEMP%\cred_input.txt
echo.>>%TEMP%\cred_input.txt

for /f "tokens=2 delims==" %%a in ('type %TEMP%\cred_input.txt ^| git credential fill ^| findstr "password="') do set TOKEN=%%a
if not "%TOKEN%"=="" (
    curl -s -X POST "https://api.github.com/user/repos" -H "Authorization: Bearer %TOKEN%" -H "Accept: application/vnd.github+json" -H "Content-Type: application/json" -d "{\"name\":\"VulnSight\",\"description\":\"AI-powered vulnerability report analyzer\",\"public\":true}"
    echo.
    echo Token found, pushing...
    cd /d C:\Users\HZR\Desktop\VulnSight
    git remote add origin https://xiabai2004:%TOKEN%@github.com/xiabai2004/VulnSight.git 2>nul
    git push -u origin master
) else (
    echo No token found
)
