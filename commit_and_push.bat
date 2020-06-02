cd /D "%~dp0"
git add -A
git status
git commit -m "Data updated - %date%"
git push
cmd /k