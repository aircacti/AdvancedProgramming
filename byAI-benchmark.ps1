$JobCount = 50
$ConsumerVariants = @(8, 15, 30)
$WorkTimeSeconds = 10
$QueueName = "jobs"
$RabbitPort = 8081
$ApiUrl = "http://localhost:8080/api"
$TimeoutSeconds = 600

Set-Location $PSScriptRoot

$authBytes = [System.Text.Encoding]::ASCII.GetBytes("guest:guest")
$authHeader = @{ Authorization = "Basic " + [Convert]::ToBase64String($authBytes) }

$resetScript = @"
import pika

params = pika.ConnectionParameters(host='localhost', port=$RabbitPort)
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='$QueueName', durable=True)
channel.queue_purge(queue='$QueueName')
connection.close()
"@

function Get-QueueState {
    try {
        $queues = Invoke-RestMethod -Uri "$ApiUrl/queues" -Headers $authHeader -TimeoutSec 10
    }
    catch {
        return $null
    }

    $queue = $queues | Where-Object { $_.name -eq $QueueName }
    if ($null -eq $queue) {
        return $null
    }

    $ready = 0
    if ($null -ne $queue.messages_ready) {
        $ready = [int]$queue.messages_ready
    }

    $unacked = 0
    if ($null -ne $queue.messages_unacknowledged) {
        $unacked = [int]$queue.messages_unacknowledged
    }

    return [PSCustomObject]@{
        Ready   = $ready
        Unacked = $unacked
        Total   = $ready + $unacked
    }
}

Write-Host "Sprawdzam brokera na $ApiUrl ..."
try {
    Invoke-RestMethod -Uri "$ApiUrl/overview" -Headers $authHeader -TimeoutSec 10 | Out-Null
}
catch {
    Write-Host "Nie moge sie polaczyc z panelem RabbitMQ."
    Write-Host "Uruchom brokera komenda: docker compose up -d"
    exit 1
}

$results = @()
$consumers = @()

try {
    foreach ($consumerCount in $ConsumerVariants) {
        Write-Host ""
        Write-Host "=== Wariant: $consumerCount konsumentow ==="

        Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 2

        $resetScript | python -
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Nie udalo sie wyczyscic kolejki. Pomijam wariant."
            continue
        }

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

            $state = Get-QueueState
            if ($null -ne $state) {
                $doneCount = $JobCount - $state.Total
            }

            $elapsed = [math]::Round($stopwatch.Elapsed.TotalSeconds)
            Write-Host -NoNewline ("`rGotowe: $doneCount/$JobCount " +
                "(w kolejce: $($state.Ready), w robocie: $($state.Unacked)) ($elapsed s)")

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
            Write-Host "PRZEKROCZONO LIMIT CZASU - sprawdz, czy consumer.py sie uruchamia"
            Write-Host "i czy port $RabbitPort jest tym samym, ktory ustawiles w skryptach."
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
}

Write-Host ""
Write-Host "=== WYNIKI ($JobCount prac, $WorkTimeSeconds s na prace) ==="
$results | Format-Table -AutoSize
$results | Export-Csv "byAI-benchmark_results.csv" -NoTypeInformation -Encoding UTF8
