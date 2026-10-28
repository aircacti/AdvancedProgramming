# Benchmark kolejki: ile trwa wykonanie wszystkich prac
# przy roznej liczbie konsumentow.

$JobCount = 50
$ConsumerVariants = @(8, 15, 30)
$WorkTimeSeconds = 10   # musi sie zgadzac z time.sleep(...) w consumer.py
$QueueFile = "queue.txt"   # musi sie zgadzac z QUEUE_FILE w consumer.py
$LockFile = "lock.txt"     # musi sie zgadzac z LOCK_FILE w consumer.py
$TimeoutSeconds = 600   # przerwij wariant, jesli trwa dluzej niz 10 minut

# Pracujemy w katalogu, w ktorym lezy ten skrypt
Set-Location $PSScriptRoot

$results = @()
$consumers = @()

try {
    foreach ($consumerCount in $ConsumerVariants) {
        Write-Host ""
        Write-Host "=== Wariant: $consumerCount konsumentow ==="

        # 1. Reset kolejki
        Remove-Item $QueueFile -ErrorAction SilentlyContinue
        Remove-Item $LockFile -Recurse -ErrorAction SilentlyContinue

        # 2. Wrzucenie prac
        Write-Host "Dodaje $JobCount prac..."
        for ($i = 1; $i -le $JobCount; $i++) {
            python producer.py | Out-Null
        }

        # 3. Start stopera i konsumentow w tle
        $stopwatch = [System.Diagnostics.Stopwatch]::StartNew()
        $consumers = @()
        for ($i = 1; $i -le $consumerCount; $i++) {
            $process = Start-Process python -ArgumentList "consumer.py" `
                -WindowStyle Hidden -PassThru
            $consumers += $process
        }

        # 4. Czekamy, az wszystkie prace beda "done"
        $doneCount = 0
        $timedOut = $false
        while ($doneCount -lt $JobCount) {
            Start-Sleep -Seconds 1

            $lines = Get-Content $QueueFile -ErrorAction SilentlyContinue
            $doneCount = 0
            foreach ($line in $lines) {
                if ($line -like "*,done") {
                    $doneCount++
                }
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

        # 5. Zatrzymanie konsumentow
        foreach ($process in $consumers) {
            Stop-Process -Id $process.Id -ErrorAction SilentlyContinue
        }
        $consumers = @()

        if ($timedOut) {
            Write-Host "PRZEKROCZONO LIMIT CZASU - sprawdz nazwy plikow"
            Write-Host "i czy consumer.py sie uruchamia. Pomijam wariant."
            continue
        }

        # 6. Zapisanie wyniku wariantu
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
    # Wykona sie tez po Ctrl+C, wiec nie zostana ukryte procesy w tle
    foreach ($process in $consumers) {
        Stop-Process -Id $process.Id -ErrorAction SilentlyContinue
    }
    Remove-Item $LockFile -Recurse -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "=== WYNIKI ($JobCount prac, $WorkTimeSeconds s na prace) ==="
$results | Format-Table -AutoSize
$results | Export-Csv "byAI-benchmark_results.csv" -NoTypeInformation -Encoding UTF8