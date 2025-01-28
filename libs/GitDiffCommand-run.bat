@echo off
REM Batch file to execute the Python git diff script

REM Path to Python executable
set PYTHON_EXEC=python

REM Path to the Python script
set SCRIPT_PATH=GitDiffCommand.py

REM Arguments for the script
set COMMIT_FROM=commit1
set COMMIT_TO=commit2
set EXTENSIONS=py js
set EXCLUDE_PATHS=dir1 file2

REM Run the Python script
%PYTHON_EXEC% %SCRIPT_PATH% %COMMIT_FROM% %COMMIT_TO% --extensions %EXTENSIONS% --exclude %EXCLUDE_PATHS%

pause
