﻿param(
[string]$path)

#Get-WmiObject -Class Win32_Product -Computer . | Select-Object Name, Version | Out-File -FilePath $path -Encoding ascii
$regpath = 'HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall'
$regpath2 = 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall'
$version = Get-ItemProperty "$regpath\*" | Select-Object DisplayName, DisplayVersion | Out-File -FilePath $path -Encoding ascii
$version = Get-ItemProperty "$regpath2\*" | Select-Object DisplayName, DisplayVersion | Out-File -FilePath $path -Encoding ascii

#Write-Host $version