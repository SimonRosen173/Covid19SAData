cd /D "%~dp0"
git pull
F:\ProgramData\Anaconda\python.exe update_site.py
echo "update_site.py finished"
commit_and_push.bat
echo "commit_and_push.bat finished"