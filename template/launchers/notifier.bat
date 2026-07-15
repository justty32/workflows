@echo off
REM 單獨起 routines 的「通知 daemon」（notifier）。
REM 通常不用手動：daemon.bat 起主 daemon 時會偵測 notifier 沒開就一起開。
REM 這支是想單獨跑 / 重開 notifier 時用。
REM 前提：PowerShell 在 PATH 上（Windows 內建）。
title routines-notifier
powershell -NoExit -ExecutionPolicy Bypass -File "{{repo 絕對路徑}}\notifier\notifier.ps1"
