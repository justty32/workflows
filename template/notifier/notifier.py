#!/usr/bin/env python3
# notifier.py — routines 常駐精靈的「通知 daemon」terminal 版（跨平台：Linux / macOS / Windows）
#
# 跟 PowerShell 版 notifier.ps1 同一套 state/ 檔案協定，只是用 Python 實作、呈現在 terminal 選單。
# 設計見 workflows/routines/design.md「通知 daemon」段。這支程式沒有判斷力，一切靈活性都在主
# agent 傳來的 state/notify.json 消息裡。職責：
#   1. 輪詢 state/notify.json（主 agent 的通知請求 {id, message, options}）→ 進記憶體佇列、刪檔
#   2. terminal 顯示 message + 編號選單（每項顯示「簡述 → 實際指令」）
#   3. 依打的編號跑對應指令（一次可多個編號；可另帶自由文字）
#   4. 把選擇 / 自由文字寫回 state/reply.json，回傳主 agent
# 托底：Ctrl-C / 結束時把佇列剩餘 dump 到 state/pending.json，主 agent 下次啟動撿回。
#
# 前提：Python 3.9+（用到 zoneinfo；系統缺 tzdata 時自動退回本地時間）。

import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

TZ = '{{時區，如 Asia/Taipei}}'   # 〔模板〕IANA 時區名（跟 PowerShell 版的 Windows 時區 ID 不同）
POLL_SECONDS = 2

ROOT = Path(__file__).resolve().parent.parent   # notifier/ 的上一層 = repo 根
STATE = ROOT / 'state'
NOTIFY = STATE / 'notify.json'
REPLY = STATE / 'reply.json'
PENDING = STATE / 'pending.json'


def stamp():
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo(TZ)).strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')   # 缺 tzdata → 退回本地時間


def read_json(path, default):
    try:
        return json.loads(path.read_text(encoding='utf-8'))   # 強制 UTF-8
    except Exception:
        return default   # 可能主 agent 還在寫、或檔壞 → 這輪略過


def append_reply(obj):
    # daemon 只 append，清空由主 agent 讀完負責
    existing = read_json(REPLY, [])
    if not isinstance(existing, list):
        existing = [existing]
    existing.append(obj)
    REPLY.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding='utf-8')


def opt_pair(o):
    # 每個 option 是單鍵物件 {簡述: 實際指令}
    key = next(iter(o.keys()))
    return key, str(o[key])


def run_cmd(cmd):
    # 跑選中的指令（exit 0 / 空 = 啥都不做，略過）。在新 terminal 跑，好讓 claude 這種互動指令有 TTY；
    # 找不到 terminal emulator（headless）就背景跑、輸出丟 state/notifier-run.log。
    cmd = cmd.strip()
    if cmd == '' or cmd == 'exit 0':
        return False
    if os.name == 'nt':
        subprocess.Popen(['powershell', '-NoExit', '-Command', cmd])
        return True
    term = os.environ.get('TERMINAL')
    candidates = ([term] if term else []) + ['x-terminal-emulator', 'gnome-terminal', 'konsole', 'xfce4-terminal', 'xterm']
    for t in candidates:
        if t and shutil.which(t):
            try:
                # emulator 的旗標語法不一（gnome-terminal 用 `--`、其餘多用 `-e`）；不合你的 emulator 就改這裡
                if os.path.basename(t) == 'gnome-terminal':
                    subprocess.Popen([t, '--', 'bash', '-lc', f'{cmd}; exec bash'])
                else:
                    subprocess.Popen([t, '-e', 'bash', '-lc', f'{cmd}; exec bash'])
                return True
            except Exception:
                continue
    log = STATE / 'notifier-run.log'
    with open(log, 'a', encoding='utf-8') as f:
        subprocess.Popen(['bash', '-lc', cmd], stdout=f, stderr=f, start_new_session=True)
    print(f'[notifier] 無 terminal emulator，改背景執行（log: {log}）')
    return True


def process(msg):
    opts = msg.get('options') or []
    pairs = [opt_pair(o) for o in opts]
    print()
    print('==================== 通知 ====================')
    print(msg.get('message', ''))
    print('----------------------------------------------')
    for i, (desc, cmd) in enumerate(pairs, 1):
        print(f'  [{i}] {desc}')
        print(f'        → {cmd}')
    print('  [0] 啥都不做（或直接 Enter）')
    print('----------------------------------------------')
    print('打編號（可空格分隔多個）；可另接自由文字，會一併回傳主 agent。')
    raw = input('選擇> ')

    # 解析：整數 token = 選項編號，其餘 join 成自由文字
    chosen, free_bits = [], []
    for tok in raw.replace(',', ' ').split():
        if tok.isdigit() and 1 <= int(tok) <= len(pairs):
            chosen.append(int(tok))
        else:
            free_bits.append(tok)
    chosen = list(dict.fromkeys(chosen))   # 去重、保序
    free_text = ' '.join(free_bits).strip()

    ran = []
    for n in chosen:
        _, cmd = pairs[n - 1]
        try:
            if run_cmd(cmd):
                print(f'[notifier] 執行：{cmd.strip()}')
                ran.append(cmd.strip())
        except Exception as e:
            print(f'[notifier] 執行失敗：{e}')

    # 回寫 reply.json 給主 agent（不論有沒有選都回，讓 agent 知道我回應過）
    append_reply({
        'id': msg.get('id'),
        'tsLocal': stamp(),
        'chosen': chosen,
        'ranCommands': ran,
        'freeText': free_text,
    })


def save_pending(queue):
    if not queue:
        return
    existing = read_json(PENDING, [])
    if not isinstance(existing, list):
        existing = [existing]
    existing.extend(queue)
    PENDING.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'\n[notifier] 已把 {len(queue)} 則未處理消息存到 state/pending.json，主 agent 下次啟動會撿回。')


def main():
    STATE.mkdir(exist_ok=True)
    queue = []
    print(f'[notifier] routines 通知 daemon（Python terminal 版）啟動（每 {POLL_SECONDS}s 輪詢 state/notify.json）。Ctrl-C 結束會 dump 未處理消息。')
    print(f'[notifier] repo 根：{ROOT}')
    try:
        while True:
            # 收信：notify.json 存在就讀進佇列、刪檔（讀到一半 → None，留著下輪再讀）
            if NOTIFY.exists():
                incoming = read_json(NOTIFY, None)
                if incoming is not None:
                    try:
                        NOTIFY.unlink()
                    except FileNotFoundError:
                        pass
                    queue.append(incoming)
            # 處理佇列：一次一則、阻塞式選單（等我回）
            while queue:
                process(queue[0])
                queue.pop(0)
            time.sleep(POLL_SECONDS)
    except KeyboardInterrupt:
        pass
    finally:
        save_pending(queue)


if __name__ == '__main__':
    sys.exit(main())
