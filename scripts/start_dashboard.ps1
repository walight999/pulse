# Start the Streamlit dashboard
$projectDir = Split-Path -Parent $PSScriptRoot
Set-Location $projectDir
streamlit run dashboard.py
