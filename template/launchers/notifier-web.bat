@echo off
REM 單獨起 / 重開 routines 通知 daemon 的「網頁版」server，並開瀏覽器到提醒頁。
REM 通常不用手動：daemon.bat 起主 daemon 時會偵測 notifier 沒開就一起帶起網頁版。
REM 前提：PowerShell 在 PATH 上（Windows 內建）；提醒頁在 http://127.0.0.1:8787/
start "routines-notifier" powershell -NoExit -ExecutionPolicy Bypass -File "{{repo 絕對路徑}}\notifier\notifier-web.ps1"
timeout /t 2 /nobreak >NUL 2>&1
start "" http://127.0.0.1:8787/
