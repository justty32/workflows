#!/usr/bin/env bash
# 開工時跑這個（或桌面捷徑指向它），起一個「常駐」的 Claude Code session：
# 用 /loop 每 30 分喚醒一次跑 /tick（判當地時段、讀 state/inbox.md、發短提醒）。
# 要盯緊時可在 session 內改跑 /loop 5m /tick，或臨時改這行的間隔。
# 前提：claude CLI 已裝好並在 PATH；notifier 需要 python3。
cd "{{repo 絕對路徑}}" || exit 1

# 順手偵測「通知 daemon」（notifier）開了沒——靠 pgrep 找 notifier.py；沒開就一起帶起 terminal 版，
# 省得兩支分別啟動。headless（無 terminal emulator）時改請你自己在另一個 terminal 跑 notifier.sh。
if ! pgrep -f 'notifier/notifier.py' >/dev/null 2>&1; then
  echo "[daemon] notifier 沒在跑，嘗試起 terminal 版..."
  NPATH="{{repo 絕對路徑}}/notifier/notifier.py"
  if [ -n "$TERMINAL" ] && command -v "$TERMINAL" >/dev/null 2>&1; then
    "$TERMINAL" -e bash -lc "python3 '$NPATH'" &
  elif command -v x-terminal-emulator >/dev/null 2>&1; then
    x-terminal-emulator -e bash -lc "python3 '$NPATH'" &
  elif command -v gnome-terminal >/dev/null 2>&1; then
    gnome-terminal -- bash -lc "python3 '$NPATH'; exec bash" &
  else
    echo "[daemon] 找不到 terminal emulator；請自己在另一個 terminal 跑：launchers/notifier.sh"
  fi
else
  echo "[daemon] notifier 已在跑，略過。"
fi

claude "/loop 30m /tick" --dangerously-skip-permissions
