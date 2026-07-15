# notifier-web.ps1 — routines 通知 daemon 的「網頁版」（笨 server，非 agent）
#
# 跟 terminal 版 notifier.ps1 同一套 state\ 檔案協定，只是把提醒從 terminal 選單
# 改呈現在網頁上。刻意最輕量：PowerShell 內建 TcpListener 綁 127.0.0.1 高埠、手擼
# 極簡 HTTP，零額外安裝、也不需要 admin（HttpListener 綁非 localhost 才要 urlacl）。
# 設計見 workflows\routines\design.md「通知 daemon」段。
#
# 職責（跟 terminal 版一致）：
#   收信  ：GET /api/pending 時讀 state\notify.json 進記憶體佇列、刪檔
#   呈現  ：GET / 回一頁醜 HTML，JS 每 2s 輪詢 /api/pending 渲染訊息 + 選項
#   回覆  ：POST /api/reply → 跑我勾選的指令（新視窗）→ append state\reply.json → 移出佇列
#   托底  ：佇列存記憶體；Ctrl-C 結束把剩下的 dump 到 state\pending.json
#
# 好處：資訊存 server 端，手滑關掉瀏覽器分頁也不丟（重開網頁又看得到）。

$ErrorActionPreference = 'Stop'
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch {}

$TimeZoneId  = '{{時區 ID，例 Taipei Standard Time}}'    # 〔模板〕改成你的 Windows 時區 ID
$Root        = Split-Path -Parent $PSScriptRoot          # notifier\ 的上一層 = repo 根
$StateDir    = Join-Path $Root 'state'
$NotifyFile  = Join-Path $StateDir 'notify.json'
$ReplyFile   = Join-Path $StateDir 'reply.json'
$PendingFile = Join-Path $StateDir 'pending.json'
$Port        = 8787

# in-memory 佇列：收到但還沒回覆的消息（正規化成 {id, message, options:[{desc,cmd}]}）
$queue = [System.Collections.Generic.List[object]]::new()

function Get-Stamp {
    [System.TimeZoneInfo]::ConvertTimeBySystemTimeZoneId((Get-Date), $TimeZoneId).ToString('yyyy-MM-dd HH:mm:ss')
}

# 讀 notify.json 進佇列、刪檔（每次有請求進來時做，等於 lazy 收信）
function Read-Notify {
    if (-not (Test-Path $NotifyFile)) { return }
    try {
        $incoming = Get-Content -Raw -Encoding UTF8 -Path $NotifyFile | ConvertFrom-Json   # 強制 UTF-8，免 5.1 把無 BOM 中文當 ANSI
        Remove-Item -Path $NotifyFile -Force
        if (-not $incoming) { return }
        $opts = @()
        foreach ($o in @($incoming.options)) {
            $p = $o.PSObject.Properties | Select-Object -First 1   # 單鍵物件 {簡述: 指令}
            $opts += [pscustomobject]@{ desc = $p.Name; cmd = "$($p.Value)" }
        }
        $queue.Add([pscustomobject]@{ id = "$($incoming.id)"; message = "$($incoming.message)"; options = $opts })
    } catch {
        # 主 agent 可能寫到一半，這次略過、下個請求再讀
    }
}

# append 一則回覆到 reply.json（server 只 append，清空由主 agent 讀完負責）
function Add-Reply($obj) {
    $existing = @()
    if (Test-Path $ReplyFile) {
        try { $existing = @(Get-Content -Raw -Path $ReplyFile | ConvertFrom-Json) } catch { $existing = @() }
    }
    $all = @($existing) + @($obj)
    $all | ConvertTo-Json -Depth 12 | Set-Content -Path $ReplyFile -Encoding UTF8
}

# 跑一條指令（exit 0 / 空 = 啥都不做，略過）；在新視窗跑、別卡住 server
function Start-Cmd($cmd) {
    $cmd = "$cmd".Trim()
    if ($cmd -eq '' -or $cmd -eq 'exit 0') { return $false }
    Start-Process -FilePath 'powershell' -ArgumentList '-NoExit', '-Command', $cmd | Out-Null
    return $true
}

# Ctrl-C / 結束時把佇列剩餘 dump 到 pending.json（附既有、不覆蓋）
function Save-Pending {
    if ($queue.Count -le 0) { return }
    $existing = @()
    if (Test-Path $PendingFile) {
        try { $existing = @(Get-Content -Raw -Path $PendingFile | ConvertFrom-Json) } catch { $existing = @() }
    }
    ($existing + $queue.ToArray()) | ConvertTo-Json -Depth 12 | Set-Content -Path $PendingFile -Encoding UTF8
    Write-Host "`n[notifier-web] 已把 $($queue.Count) 則未回覆消息存到 state\pending.json，主 agent 下次啟動撿回。" -ForegroundColor Yellow
}

# 一頁醜 HTML（單引號 here-string = 純文字、不做 PowerShell 變數插補）
$Html = @'
<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<title>routines 通知</title>
<style>
 body{font-family:Consolas,monospace;margin:1em;background:#111;color:#ddd}
 h3{margin:.2em 0}
 .msg{border:1px solid #555;padding:.6em .8em;margin:.7em 0;background:#1a1a1a}
 .txt{margin-bottom:.5em;white-space:pre-wrap}
 .cmd{color:#888;font-size:.85em}
 label{display:block;margin:.15em 0}
 input[type=text]{background:#000;color:#ddd;border:1px solid #555;padding:.2em;width:24em}
 button{margin:.3em .3em 0 0;background:#333;color:#ddd;border:1px solid #666;padding:.3em .7em;cursor:pointer}
 #st{color:#666;font-size:.8em}
</style></head>
<body>
<h3>routines 通知</h3>
<div id="st">連線中…</div>
<div id="app"></div>
<script>
let lastSig = undefined;
function esc(s){return (s==null?'':String(s)).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function asArr(x){return Array.isArray(x)?x:(x==null?[]:[x]);}
function render(arr){
  const app=document.getElementById('app');
  if(arr.length===0){app.innerHTML='<p style="color:#666">（目前無通知）</p>';return;}
  app.innerHTML=arr.map(m=>{
    const opts=asArr(m.options).map((o,i)=>{
      const noop=((o.cmd==null?'':o.cmd)+'').trim()==='exit 0';   // 放掉項（exit 0）跟行動項互斥
      return `<label><input type="checkbox" name="opt" value="${i}" data-noop="${noop?1:0}" onchange="excl(this)"> ${esc(o.desc)} <span class="cmd">→ ${esc(o.cmd)}</span></label>`;
    }).join('');
    return `<div class="msg">
      <div class="txt">${esc(m.message)}</div>
      <form onsubmit="return sendReply(this,'${esc(m.id)}')">
        ${opts}
        <div><input type="text" name="free" placeholder="自由文字（可留空，會回傳主 agent）"></div>
        <button type="submit">送出</button>
        <button type="button" onclick="nothing('${esc(m.id)}')">啥都不做</button>
      </form>
    </div>`;
  }).join('');
}
async function poll(){
  try{
    const r=await fetch('/api/pending'); const arr=asArr(await r.json());
    document.getElementById('st').textContent='已連線 · '+arr.length+' 則待處理 · '+new Date().toLocaleTimeString();
    const sig=arr.map(m=>m.id).join('|');
    if(sig!==lastSig){lastSig=sig;render(arr);}   // 集合沒變就不重繪，免清掉正在打的字
  }catch(e){ document.getElementById('st').textContent='server 沒回應（可能已關）'; }
}
async function post(id,chosen,free){
  await fetch('/api/reply',{method:'POST',headers:{'Content-Type':'application/json'},
    body:JSON.stringify({id:id,chosen:chosen,freeText:free})});
  lastSig=undefined; poll();   // 強制重繪
}
function excl(cb){   // 放掉項(exit 0)與行動項互斥；自由文字不受影響
  const form=cb.closest('form'); if(!cb.checked) return;
  if(cb.dataset.noop==='1'){ form.querySelectorAll('input[name=opt]').forEach(x=>{ if(x!==cb) x.checked=false; }); }
  else { form.querySelectorAll('input[name=opt][data-noop="1"]').forEach(x=>{ x.checked=false; }); }
}
function sendReply(form,id){
  const chosen=[...form.querySelectorAll('input[name=opt]:checked')].map(c=>parseInt(c.value,10));
  post(id,chosen,form.querySelector('input[name=free]').value); return false;
}
function nothing(id){ post(id,[],''); }
setInterval(poll,2000); poll();
</script>
</body></html>
'@

# 寫一個 HTTP 回應到 socket（body 用 UTF-8）
function Send-Http($stream, $status, $contentType, $bodyString) {
    $bodyBytes   = [System.Text.Encoding]::UTF8.GetBytes($bodyString)
    $header      = "HTTP/1.1 $status`r`nContent-Type: $contentType; charset=utf-8`r`nContent-Length: $($bodyBytes.Length)`r`nConnection: close`r`n`r`n"
    $headerBytes = [System.Text.Encoding]::ASCII.GetBytes($header)
    $stream.Write($headerBytes, 0, $headerBytes.Length)
    $stream.Write($bodyBytes, 0, $bodyBytes.Length)
    $stream.Flush()
}

$listener = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $Port)
$listener.Start()
try { $Host.UI.RawUI.WindowTitle = 'routines-notifier' } catch {}   # 供 daemon.bat 偵測是否已開
Write-Host "[notifier-web] routines 通知 daemon（網頁版）啟動：http://127.0.0.1:$Port/" -ForegroundColor Cyan
Write-Host "[notifier-web] repo 根：$Root ；Ctrl-C 結束會 dump 未回覆消息。"

try {
    while ($true) {
        $client = $listener.AcceptTcpClient()
        try {
            $stream = $client.GetStream()
            $stream.ReadTimeout = 5000

            # 逐 byte 讀到 \r\n\r\n 取得 header（headers 很小，localhost 個人用夠快）
            $hb = [System.Collections.Generic.List[byte]]::new()
            $one = New-Object byte[] 1
            while ($true) {
                $n = $stream.Read($one, 0, 1)
                if ($n -le 0) { break }
                $hb.Add($one[0])
                $c = $hb.Count
                if ($c -ge 4 -and $hb[$c-4] -eq 13 -and $hb[$c-3] -eq 10 -and $hb[$c-2] -eq 13 -and $hb[$c-1] -eq 10) { break }
            }
            $headerText = [System.Text.Encoding]::ASCII.GetString($hb.ToArray())
            $lines = $headerText -split "`r`n"
            $reqLine = $lines[0]
            $parts   = $reqLine -split ' '
            $method  = $parts[0]
            $path    = if ($parts.Count -ge 2) { $parts[1] } else { '/' }

            # body 依 Content-Length 讀「位元組」（別用 StreamReader 讀 char，中文會對不上）
            $contentLength = 0
            foreach ($l in $lines) { if ($l -match '^(?i)Content-Length:\s*(\d+)') { $contentLength = [int]$Matches[1] } }
            $body = ''
            if ($contentLength -gt 0) {
                $bodyBuf = New-Object byte[] $contentLength
                $read = 0
                while ($read -lt $contentLength) {
                    $n = $stream.Read($bodyBuf, $read, $contentLength - $read)
                    if ($n -le 0) { break }
                    $read += $n
                }
                $body = [System.Text.Encoding]::UTF8.GetString($bodyBuf, 0, $read)
            }

            # 路由
            if ($path -like '/api/pending*') {
                Read-Notify
                $json = @($queue) | ConvertTo-Json -Depth 12
                if (-not $json) { $json = '[]' }
                Send-Http $stream '200 OK' 'application/json' $json
            }
            elseif ($path -like '/api/reply*') {
                try {
                    $reply  = $body | ConvertFrom-Json
                    $rid    = "$($reply.id)"
                    $msg    = $queue | Where-Object { $_.id -eq $rid } | Select-Object -First 1
                    $chosen = @($reply.chosen)
                    $ran    = @()
                    if ($msg) {
                        foreach ($idx in $chosen) {
                            $opt = @($msg.options)[[int]$idx]
                            if ($opt -and (Start-Cmd $opt.cmd)) { $ran += $opt.cmd }
                        }
                    }
                    Add-Reply ([ordered]@{
                        id          = $rid
                        tsLocal     = Get-Stamp
                        chosen      = @($chosen | ForEach-Object { [int]$_ + 1 })   # 存 1-based，跟 terminal 版一致
                        ranCommands = @($ran)
                        freeText    = "$($reply.freeText)"
                    })
                    # 依 id 移出佇列（別靠參考相等，較穩）
                    for ($k = $queue.Count - 1; $k -ge 0; $k--) {
                        if ("$($queue[$k].id)" -eq $rid) { $queue.RemoveAt($k) }
                    }
                    Send-Http $stream '200 OK' 'application/json' '{"ok":true}'
                } catch {
                    Send-Http $stream '400 Bad Request' 'application/json' '{"ok":false}'
                }
            }
            elseif ($method -eq 'GET') {
                Send-Http $stream '200 OK' 'text/html' $Html
            }
            else {
                Send-Http $stream '404 Not Found' 'text/plain' 'not found'
            }
        } catch {
            # 單一請求出錯不弄垮 server
        } finally {
            $client.Close()
        }
    }
} finally {
    Save-Pending
    $listener.Stop()
}
