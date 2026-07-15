@echo off
REM 開工時雙擊這個（或桌面指向它的捷徑），起一個「常駐」的 Claude Code session：
REM 用 /loop 每 30 分喚醒一次跑 /tick（判當地時段、讀 state\inbox.md、發短提醒）。
REM 要盯緊時可在 session 內改跑 /loop 5m /tick，或臨時改這行的間隔。
REM 前提：claude CLI 已裝好並在 PATH 上。
cd /d "{{repo 絕對路徑}}"

REM 順手偵測「通知 daemon」（notifier）開了沒——靠視窗標題 routines-notifier；沒開就一起帶起網頁版，
REM 省得兩支分別啟動。網頁版提醒頁在 http://127.0.0.1:8787/（想用 terminal 版改指向 notifier.ps1）。
tasklist /FI "WINDOWTITLE eq routines-notifier" 2>NUL | find /I "powershell" >NUL
if errorlevel 1 (
  echo [daemon] notifier 沒在跑，幫忙起網頁版 http://127.0.0.1:8787/ ...
  start "routines-notifier" powershell -NoExit -ExecutionPolicy Bypass -File "{{repo 絕對路徑}}\notifier\notifier-web.ps1"
  timeout /t 2 /nobreak >NUL 2>&1
  start "" http://127.0.0.1:8787/
) else (
  echo [daemon] notifier 已在跑，略過。
)

claude "/loop 30m /tick" --dangerously-skip-permissions
