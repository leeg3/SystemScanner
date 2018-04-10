"""
Author: Greg Lee
Date: 3/24/18
Class: Scripting for Cyber Security
Purpose: System vulnerability scanner for Mac/Windows

notes:
steps for script:
get list o updates
check to see if certain critical updates are missing
then output names of missing updates

*MAC*
seapea, achilles, aeris, dark matter, nightskies, triton, dark mullet
get list o updates
- **use this: /usr/sbin/system_profiler SPInstallHistoryDataType
- this works too kinda softwareupdate -l

check to see if certain critical updates are missing
- apple does not say which update patched these vulnerabilities but it was patched in all Mac's made after 2013.
- need to get a list of updates that were made specifically for these exploits
- compare list from above to list of installed updates
https://support.apple.com/en-us/HT201222

then output names of missing updates

prompt for script to automatically install it?
- sudo softwareupdate -i <name of update>
done


*Windows*
AngelFire (Xp/7), Dumbo (x32 XP/Vista/new versions), BothanSpy, Elsa, Brutal Kangaroo,
Pandemic, Athena (XP and up), AfterMidnight, Grasshopper

get list of updates
see ps script

check for missing updates
- get list o updates for Vault 7

output names of missing updates

prompt script to automatically install?
- looks like i'd need to do this to auto install updates
https://gallery.technet.microsoft.com/scriptcenter/2d191bcd-3308-4edd-9de2-88dff796b0bc
"""

import os
import platform

# seapea[10.6, 10.7], achilles [10.6, all?], nightskies[10.5], triton [10.7, 10.8], dark mullet, Der Stare[10.8, 10.9]
# aeris[malware], Sonic Screwdriver[firmware thing]
# just update to 10.10 with latest Security updates?
# Apple said the things mentioned here have been patched since 2013
# Source: https://www.macrumors.com/2017/03/07/apple-wikileaks-vault-7-patched/

def MacScanner():
    # get updates from system
    minVersion = "10.20" # CHANGE BACK TO 10.10
    minSecurityUpdateVersion = [2017, 3] #OG 2015, 6

    print("Mac System Scanner")

    os.system("defaults read loginwindow SystemVersionStampAsString > SystemVersion.txt")

    # check system OS. if older than 10.10 then proceed with updates check
    print("Getting System OS version:")
    OS_version = [OS_version.rstrip('\n') for OS_version in open('SystemVersion.txt')]
    print(OS_version[0] + '\n')

    current_os = OS_version[0].split('.')
    secure_os= minVersion.split('.')

    if int(current_os[1]) > int(secure_os[1]):
        print("Your Operating System is safe from Vault 7 exploits.\n")
        return
    else:
        print("Your Operating System is vulnerable to some Vault 7 exploits, please upgrade to your OS.\n")

    print("Retrieving list of installed system updates")
    os.system("/usr/sbin/system_profiler SPInstallHistoryDataType > InstalledUpdates.txt")
    # open file and get the update name and the version #
    # can prob use algoirthm from CA to get the info
    # check against array of most up to date version numbers of important updates
    # output update names and version numbers that are less than the ones in the array
    lines = [line.rstrip('\n') for line in open('InstalledUpdates.txt')]

    for i in range(0, len(lines)):
        lines[i] = lines[i].strip()

        if lines[i] == '\n' or lines[i] == "":
            i += 1

    update_names = []
    update_version_num = []

    for i in range(0, len(lines)):
        # print(lines[i])
        if "Security Update" in lines[i] and "Security Update" not in update_names:
            update_names.append(lines[i].rstrip(':'))

    print("The following Security Updates have been installed onto this machine: ")

    for elem in update_names:
        print(elem)

    for i in range(0, len(update_names)):
        # print(update_names[i])
        update_version_num.append(update_names[i].split(' '))

    uptodate_update = 0
    uptodate_version = 0

    for value in update_version_num:
        temp = value[2].split('-')

        if int(temp[0]) > minSecurityUpdateVersion[0]:
            # print("its a new security update")
            uptodate_update = 1
        elif int(temp[0]) == int(minSecurityUpdateVersion[0]):
            if int(temp[1]) > int(minSecurityUpdateVersion[1]):
                # print("its a new security version")
                uptodate_version = 1

    if uptodate_update == 1 and uptodate_version == 1:
        print("Your system is secure from most Vault 7 mac OS X vulnerabilties")
    elif uptodate_version == 0:
        print("Please apply the newest version of the security update to your machine")
    else:
        print("Please update OS to newest version")


# AngelFire (Xp/7), Dumbo (x32 XP/Vista/new versions), BothanSpy(all), Elsa (all), Brutal Kangaroo(XP), Pandemic(all), Athena (XP and up), AfterMidnight(all), Grasshopper(>=8/all)


def WindowsScanner():

    path = os.popen('cd').read()
    path = path.rstrip('\n')

# Application Checker
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

    print("Windows Application Scanner")

    # exec script in PS with path given
    full_path = ''.join(['Powershell.exe .\Windows\getappversions.ps1 ', path, '\Windows\AppVersions.txt'])

    # get patched versions of apps from file
    patched_versions = [patched_versions.rstrip('\n').split(': ') for patched_versions in open('Windows\Patched_versions.txt')]

    # get all apps listed in vault 7 thing
    vulnerable_apps = [vulnerable_apps.rstrip('\n') for vulnerable_apps in open('Windows\vulnerable_apps.txt')]

    # get installed apps from text file generated by above PS command
    app_contents = [app_contents.rstrip('\n') for app_contents in open('Windows\AppVersions.txt')]

    app_info = []
    app_sorted = []

    # remove empty elements in list and remove excess whitespace
    for line in app_contents:
        if line != '':
            app_info.append(' '.join(line.split()))

    # separate version # and app name
    for line in app_info:
        for i in range(1, len(line)):
            if line[-i] == ' ':
                v_start = len(line) - i
                app_sorted.append([line[0:v_start].strip(), line[v_start+1:len(line)]])
                break

    update_apps = []
    num = 0

    # look for appps that need to be updated.
    print("Application Scanner")
    for installed_app in app_sorted:
        for patched_app in patched_versions:
            if patched_app[0] == installed_app[0]:
                installed_version = installed_app[1].split('.')
                patched_version = patched_app[1].split('.')

                if int(installed_version[0]) <= int(patched_version[0]):
                    num = 1
                    print("{} needs to be updated to the latest version.".format(installed_app[0]))

    if num == 0:
        print("No applications need to be updated.")

    # id and display vulnerable apps to user
    for iapp in app_sorted:
        for vapp in vulnerable_apps:
            if vapp in iapp[0] or vapp == iapp[0]:
                print('{} is vulnerable to a Vault 7 exploit. Please verify that the files are from a trusted source.'.format(iapp[0]))

# System Checker
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
    print("=======================================================")
    print("Windows System Scanner")
    os_info = os.popen('systeminfo | findstr /B /C:"OS Name" /C:"OS Version"').read()
    os_name = os_info[0].rstrip('\n')
    os_ver = os_info[1].rstrip('\n')

    print("System Information")
    print(os_info)

    affected_os = ['XP', 'Vista', '7', '8', '10']
    status = ''

    for op_sys in affected_os:
        if op_sys in os_name:
            status = 'Please update your system to the newest version of Windows. You are vulnerable to some Vault 7 exploits. '
        else:
            status = 'Your system is not vulnerable to Vault 7 exploits.'

    print(status)

    # exec script in PS with path given
    full_path = ''.join(['Powershell.exe .\Windows\getupdates.ps1 ', path, '\Windows\InstalledUpdates.txt'])

    # run PS script to get updates and put into file
    os.system(full_path)

    contents = [contents.rstrip('\n') for contents in open('Windows\InstalledUpdates.txt')]
    # print(contents)

    filtered_contents = []

    for line in contents:
        if 'Succeeded' in line or 'Title' in line:
            filtered_contents.append(line.strip())

    # print(filtered_contents)


def main():
    system_os = platform.system()

    if system_os == 'Darwin':  # Mac
        MacScanner()
    elif system_os == 'Windows':  # Windows
        WindowsScanner()


if __name__ == "__main__":
    main()
