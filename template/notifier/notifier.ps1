# notifier.ps1 — routines 常駐精靈的「通知 daemon」（笨程式，非 agent）
#
# 設計見 workflows\routines\design.md「通知 daemon」段。這支程式沒有判斷力，
# 一切靈活性都在主 agent 傳來的 state\notify.json 消息裡。職責：
#   1. 輪詢 state\notify.json（主 agent 的通知請求 {id, message, options}）
#   2. 跳 terminal 顯示 message + 編號選單（每項顯示「簡述 → 實際指令」）
#   3. 依我打的編號跑對應指令（一次可多個編號；可另帶自由文字）
#   4. 把我的選擇 / 自由文字寫回 state\reply.json，回傳主 agent
#
# 托底（清場的一半）：收到消息先存記憶體佇列；成功處理才移除；被 Ctrl-C / 關窗
#   打斷時，把佇列裡剩下沒處理的 dump 到 state\pending.json，主 agent 下次啟動撿回。
#   我若單純不理它直接關掉 → 默認當作沒回（啥都不做），不硬卡。

$ErrorActionPreference = 'Stop'
# 讓中文在 console 正常顯示（不管本機預設 codepage 是什麼）
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

$TimeZoneId  = '{{時區 ID，例 Taipei Standard Time}}'    # 〔模板〕改成你的 Windows 時區 ID
$Root        = Split-Path -Parent $PSScriptRoot          # notifier\ 的上一層 = repo 根
$StateDir    = Join-Path $Root 'state'
$NotifyFile  = Join-Path $StateDir 'notify.json'
$ReplyFile   = Join-Path $StateDir 'reply.json'
$PendingFile = Join-Path $StateDir 'pending.json'
$PollSeconds = 2

# in-memory 佇列：收到但還沒處理完的消息（FIFO）
$queue = [System.Collections.Generic.List[object]]::new()

function Get-Stamp {
    [System.TimeZoneInfo]::ConvertTimeBySystemTimeZoneId((Get-Date), $TimeZoneId).ToString('yyyy-MM-dd HH:mm:ss')
}

# Ctrl-C / 正常結束時，把佇列剩餘消息 dump 到 pending.json（附既有的，不覆蓋）
function Save-Pending {
    if ($queue.Count -le 0) { return }
    $existing = @()
    if (Test-Path $PendingFile) {
        try { $existing = @(Get-Content -Raw -Path $PendingFile | ConvertFrom-Json) } catch { $existing = @() }
    }
    $all = @($existing) + @($queue.ToArray())
    $all | ConvertTo-Json -Depth 12 | Set-Content -Path $PendingFile -Encoding UTF8
    Write-Host "`n[notifier] 已把 $($queue.Count) 則未處理消息存到 state\pending.json，主 agent 下次啟動會撿回。" -ForegroundColor Yellow
}

# 把一則回覆附加到 reply.json（daemon 只 append，清空由主 agent 讀完負責）
function Append-Reply($obj) {
    $existing = @()
    if (Test-Path $ReplyFile) {
        try { $existing = @(Get-Content -Raw -Path $ReplyFile | ConvertFrom-Json) } catch { $existing = @() }
    }
    $all = @($existing) + @($obj)
    $all | ConvertTo-Json -Depth 12 | Set-Content -Path $ReplyFile -Encoding UTF8
}

# 顯示一則消息的選單、收我的輸入、跑選中指令、回寫 reply.json
function Invoke-Message($msg) {
    $opts = @($msg.options)
    Write-Host ""
    Write-Host "==================== 通知 ====================" -ForegroundColor Cyan
    Write-Host $msg.message
    Write-Host "----------------------------------------------"
    for ($i = 0; $i -lt $opts.Count; $i++) {
        # 每個 option 是單鍵物件 {簡述: 實際指令}
        $p    = $opts[$i].PSObject.Properties | Select-Object -First 1
        $desc = $p.Name
        $cmd  = $p.Value
        Write-Host ("  [{0}] {1}" -f ($i + 1), $desc)
        Write-Host ("        → {0}" -f $cmd) -ForegroundColor DarkGray
    }
    Write-Host "  [0] 啥都不做（或直接 Enter）"
    Write-Host "----------------------------------------------"
    Write-Host "打編號（可空格分隔多個）；可另接自由文字，會一併回傳主 agent。" -ForegroundColor DarkGray
    $raw = Read-Host "選擇"

    # 解析：整數 token = 選項編號，其餘 join 成自由文字
    $chosen   = @()
    $freeBits = @()
    foreach ($tok in ($raw -split '[\s,]+' | Where-Object { $_ -ne '' })) {
        $n = 0
        if ([int]::TryParse($tok, [ref]$n) -and $n -ge 1 -and $n -le $opts.Count) {
            $chosen += $n
        } else {
            $freeBits += $tok
        }
    }
    $freeText = ($freeBits -join ' ').Trim()

    # 跑選中的指令（exit 0 / 空 = 啥都不做，略過）
    $ran = @()
    foreach ($n in ($chosen | Select-Object -Unique)) {
        $p   = $opts[$n - 1].PSObject.Properties | Select-Object -First 1
        $cmd = "$($p.Value)".Trim()
        if ($cmd -eq '' -or $cmd -eq 'exit 0') { continue }
        Write-Host "[notifier] 執行：$cmd" -ForegroundColor Green
        try {
            # 在新視窗跑，別卡住 notifier 自己的輪詢迴圈
            Start-Process -FilePath 'powershell' -ArgumentList '-NoExit', '-Command', $cmd | Out-Null
            $ran += $cmd
        } catch {
            Write-Host "[notifier] 執行失敗：$($_.Exception.Message)" -ForegroundColor Red
        }
    }

    # 回寫 reply.json 給主 agent（不論有沒有選、有沒有自由文字都回，讓 agent 知道我回應過）
    Append-Reply ([ordered]@{
        id        = $msg.id
        tsLocal   = Get-Stamp
        chosen    = @($chosen | Select-Object -Unique)
        ranCommands = @($ran)
        freeText  = $freeText
    })
}

try { $Host.UI.RawUI.WindowTitle = 'routines-notifier' } catch {}   # 供 daemon.bat 偵測是否已開
Write-Host "[notifier] routines 通知 daemon 啟動（每 ${PollSeconds}s 輪詢 state\notify.json）。Ctrl-C 結束會 dump 未處理消息。" -ForegroundColor Cyan
Write-Host "[notifier] repo 根：$Root"

try {
    while ($true) {
        # 收信：notify.json 存在就讀進佇列、刪檔（騰出槽位給下一則）
        if (Test-Path $NotifyFile) {
            try {
                $incoming = Get-Content -Raw -Encoding UTF8 -Path $NotifyFile | ConvertFrom-Json   # 強制 UTF-8，免 5.1 把無 BOM 中文當 ANSI
                Remove-Item -Path $NotifyFile -Force
                if ($incoming) { $queue.Add($incoming) }
            } catch {
                # 可能是主 agent 寫到一半，這輪略過、下輪再讀
            }
        }

        # 處理佇列：一次一則、阻塞式選單（等我回）
        while ($queue.Count -gt 0) {
            $msg = $queue[0]
            Invoke-Message $msg
            $queue.RemoveAt(0)   # 處理完才移除，未處理的留在佇列供 dump 托底
        }

        Start-Sleep -Seconds $PollSeconds
    }
} finally {
    Save-Pending
}
