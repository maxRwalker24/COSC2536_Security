<#
run_hack_auto_scan.ps1
Automatically scans a folder for all key/cipher pairs, runs Hack.exe for each, and logs results to CSV.

Requirements:
- Hack.exe in $HackFolder
- Key/cipher files in $TestFolder following pattern: key_*.txt and cipher_*.txt
- CSV output folder exists
#>

param(
    [string]$HackFolder = "C:\Testing\Hack",
    [string]$TestFolder = "C:\Testing\Cipher",
    [string]$CsvOutput = "C:\Testing\Results\hack_bench_results.csv",
    [int]$SampleIntervalMs = 200
)

# Ensure CSV header exists
if (-not (Test-Path $CsvOutput)) {
    "case_name,start_time,elapsed_s,peak_cpu_pct,peak_mem_kb" | Out-File -FilePath $CsvOutput -Encoding utf8
}

# Find all key files matching pattern
$keyFiles = Get-ChildItem -Path $TestFolder -Filter "key_*.txt"

foreach ($keyFile in $keyFiles) {
    # Derive matching cipher file: replace 'key_' with 'cipher_'
    $cipherFileName = $keyFile.Name -replace "^key_", "cipher_"
    $cipherPath = Join-Path $TestFolder $cipherFileName

    if (-not (Test-Path $cipherPath)) {
        Write-Warning "Skipping $($keyFile.Name) because matching cipher file not found."
        continue
    }

    $caseName = [System.IO.Path]::GetFileNameWithoutExtension($keyFile.Name)

    Write-Host "`n=== Running test: $caseName ==="

    # Copy key/cipher into Hack.exe folder as key.txt/cipher.txt
    Copy-Item $keyFile.FullName -Destination (Join-Path $HackFolder "key.txt") -Force
    Copy-Item $cipherPath -Destination (Join-Path $HackFolder "cipher.txt") -Force

    # Start Hack.exe interactively
    Write-Host "Starting Hack.exe for $caseName..."
    $startTime = Get-Date
    $proc = Start-Process -FilePath (Join-Path $HackFolder "Hack.exe") -PassThru -WindowStyle Normal

    # Sampling loop
    $peakCpu = 0.0
    $peakMem = 0
    $procId = $proc.Id
    $script:prevCpuTimes = @{}
    $procInfo = Get-Process -Id $procId -ErrorAction SilentlyContinue
    $script:prevCpuTimes[$procId] = @{ value = $procInfo.CPU; time = Get-Date }

    while (-not $proc.HasExited) {
        Start-Sleep -Milliseconds $SampleIntervalMs
        $p = Get-Process -Id $procId -ErrorAction SilentlyContinue
        if ($p) {
            $memKb = [math]::Round($p.WorkingSet / 1KB)
            if ($memKb -gt $peakMem) { $peakMem = $memKb }

            $prevRec = $script:prevCpuTimes[$procId]
            $nowCpu = $p.CPU
            $nowTime = Get-Date
            if ($prevRec) {
                $deltaCpu = $nowCpu - $prevRec.value
                $deltaSeconds = ($nowTime - $prevRec.time).TotalSeconds
                if ($deltaSeconds -gt 0) {
                    $procCount = 1
                    try {
                        $procCount = (Get-CimInstance Win32_Processor | Measure-Object -Property NumberOfLogicalProcessors -Sum).Sum
                        if (-not $procCount) { $procCount = 1 }
                    } catch { $procCount = 1 }
                    $deltaPct = ($deltaCpu / $deltaSeconds) * 100 / $procCount
                    if ($deltaPct -gt $peakCpu) { $peakCpu = $deltaPct }
                }
            }
            $script:prevCpuTimes[$procId] = @{ value = $nowCpu; time = $nowTime }
        }
    }

    $endTime = Get-Date
    $elapsedTime = ($endTime - $startTime).TotalSeconds

    # Append CSV
    $csvLine = ('{0},{1},{2:N3},{3:N2},{4}' -f $caseName, $startTime.ToString("o"), $elapsedTime, [math]::Round($peakCpu,2), $peakMem)
    $csvLine | Out-File -FilePath $CsvOutput -Append -Encoding utf8

    Write-Host "Test $caseName completed. Elapsed(s): $elapsedTime, PeakCPU: $([math]::Round($peakCpu,2)), PeakMem: $peakMem kB"
}

Write-Host "`nAll tests finished. CSV updated at $CsvOutput"
