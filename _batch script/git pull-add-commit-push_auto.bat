@echo off
cd ..
set "currentDate=%date%"
set "currentTime=%time%"

for /f "tokens=1-4 delims=/- " %%a in ("%currentDate%") do (
    set "year=%%a"
    set "month=00%%b"
    set "day=00%%c"
)

set month=%month:~-2%
set day=%day:~-2%
set "formattedDate=%year%-%month%-%day%"

for /f "tokens=1-3 delims=:., " %%a in ("%currentTime%") do (
    set "hour=00%%a"
    set "minute=00%%b"
    set "second=00%%c"
)

set hour=%hour:~-2%
set minute=%minute:~-2%
set second=%second:~-2%
set "formattedTime=%hour%:%minute%:%second%"

echo "[Comment]blog update at %formattedDate% T %formattedTime%"

set \p str=아무 문자열이나 입력하세요:

@echo on
pause

REM echo "htmlproofer testing..."
REM bundle exec htmlproofer _site

REM if %errorlevel% equ 0 (
    echo "[Proofer PASS]htmlproofer test passed.."
    git add -A
    git commit -m "blog update at %formattedDate% Time %formattedTime% >> %str%"

    pause

    git push origin main

REM) else (
REM    echo "[Proofer FAIL]htmlproofer test failed.."
REM    pause
REM    exit /B 1
REM)