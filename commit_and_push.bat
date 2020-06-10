cd /D "%~dp0"
git add -A
git status                              
git commit -m "[auto] Data updated - %date% %time%" 
git push
cmd /k