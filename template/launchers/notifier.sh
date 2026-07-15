#!/usr/bin/env bash
# 單獨起 / 重開 routines 的「通知 daemon」terminal 版（Python，跨平台）。
# 通常不用手動：daemon.sh 起主 daemon 時會偵測 notifier 沒開就一起開。
# 在自己的 terminal / tmux pane 裡跑（會佔用該 terminal 顯示選單、等你回）。
# 前提：python3 在 PATH。
cd "{{repo 絕對路徑}}" || exit 1
exec python3 notifier/notifier.py
