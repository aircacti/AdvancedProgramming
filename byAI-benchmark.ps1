$JobCount = 50
$ConsumerVariants = @(8, 15, 30)
$WorkTimeSeconds = 10
$DbFile = "identifier.sqlite"
$LockFile = "lock.txt"
$TimeoutSeconds = 600

Set-Location $PSScriptRoot

$results = @()
$consumers = @()

try {
    foreach ($consumerCount in $ConsumerVariants) {
        Write-Host ""
        Write-Host "=== Wariant: $consumerCount konsumentow ==="

        Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
        Start-Sleep -Milliseconds 500

        python -c "import sqlite3; con = sqlite3.connect('$DbFile', timeout=30); con.execute('DROP TABLE IF EXISTS jobs'); con.commit()" 2>$null
        Remove-Item $LockFile -Recurse -ErrorAction SilentlyContinue

        Write-Host "Dodaje $JobCount prac..."
        for ($i = 1; $i -le $JobCount; $i++) {
            python producer.py | Out-Null
        }

        $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
        $consumers = @()
        for ($i = 1; $i -le $consumerCount; $i++) {
            $process = Start-Process python -ArgumentList "consumer.py" `
                -WindowStyle Hidden -PassThru
            $consumers += $process
        }

        $doneCount = 0
        $timedOut = $false
        while ($doneCount -lt $JobCount) {
            Start-Sleep -Seconds 1

            $val = python -c "import sqlite3; con = sqlite3.connect('$DbFile', timeout=30); print(con.execute('SELECT COUNT(*) FROM jobs WHERE status=?', ('done',)).fetchone()[0])" 2>$null
            if ($val -match '^\d+$') {
                $doneCount = [int]$val
            }

            $elapsed = [math]::Round($stopwatch.Elapsed.TotalSeconds)
            Write-Host -NoNewline "`rGotowe: $doneCount/$JobCount ($elapsed s)"

            if ($elapsed -gt $TimeoutSeconds) {
                $timedOut = $true
                break
            }
        }
        $stopwatch.Stop()
        Write-Host ""

        foreach ($process in $consumers) {
            Stop-Process -Id $process.Id -ErrorAction SilentlyContinue
        }
        $consumers = @()

        if ($timedOut) {
            Write-Host "PRZEKROCZONO LIMIT CZASU - sprawdz nazwy plikow"
            Write-Host "i czy consumer.py sie uruchamia. Pomijam wariant."
            continue
        }

        $seconds = [math]::Round($stopwatch.Elapsed.TotalSeconds, 1)
        $rounds = [math]::Ceiling($JobCount / $consumerCount)
        $idealSeconds = $rounds * $WorkTimeSeconds
        $jobsPerMinute = [math]::Round($JobCount / $seconds * 60, 1)

        $results += [PSCustomObject]@{
            "Konsumenci"       = $consumerCount
            "Czas [s]"         = $seconds
            "Idealny czas [s]" = $idealSeconds
            "Prac na minute"   = $jobsPerMinute
        }
    }
}
finally {
    foreach ($process in $consumers) {
        Stop-Process -Id $process.Id -ErrorAction SilentlyContinue
    }
    Remove-Item $LockFile -Recurse -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "=== WYNIKI ($JobCount prac, $WorkTimeSeconds s na prace) ==="
$results | Format-Table -AutoSize
$results | Export-Csv "byAI-benchmark_results.csv" -NoTypeInformation -Encoding UTF8