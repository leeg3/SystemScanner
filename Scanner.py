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

    # get system info
    os.system("defaults read loginwindow SystemVersionStampAsString > SystemVersion.txt")

    # check system OS. if older than 10.10 then proceed with updates check
    print("Getting System OS version:")
    os_version = [os_version.rstrip('\n') for os_version in open('SystemVersion.txt')]
    print(os_version[0] + '\n')

    # store current OS and secure OS (patched against Vault 7) into variables
    current_os = os_version[0].split('.')
    secure_os = minVersion.split('.')

    # determine if current os is secure or not.
    if int(current_os[1]) > int(secure_os[1]):
        print("Your Operating System is safe from Vault 7 exploits.\n")
        return
    else:
        print("Your Operating System is vulnerable to some Vault 7 exploits, please upgrade to your OS.\n")

    # if the system is deemed potentially insecure, get a list of system updates
    print("Retrieving list of installed system updates")
    os.system("/usr/sbin/system_profiler SPInstallHistoryDataType > InstalledUpdates.txt")

    # parse list of installed updates into a list
    lines = [line.rstrip('\n') for line in open('InstalledUpdates.txt')]

    # remove white space from lines
    for i in range(0, len(lines)):
        lines[i] = lines[i].strip()
        if lines[i] == '\n' or lines[i] == "":
            i += 1

    # create lists to store names of updates and their current version
    update_names = []
    update_version_num = []

    # retrieve the security updates, parse them and then add into a list
    for i in range(0, len(lines)):
        if "Security Update" in lines[i] and "Security Update" not in update_names:
            update_names.append(lines[i].rstrip(':'))

    print("The following Security Updates have been installed onto this machine: ")
    for elem in update_names:
        print(elem)

    # retrieve the version numbers and store into a list
    for elem in update_names:
        update_version_num.append(elem.split(' '))

    uptodate_update = 0
    uptodate_version = 0

    # compare security update version and determine if it secures the machine
    for elem in update_version_num:
        temp = elem[2].split('-')
        if int(temp[0]) > minSecurityUpdateVersion[0]:
            uptodate_update = 1
        elif int(temp[0]) == int(minSecurityUpdateVersion[0]):
            if int(temp[1]) > int(minSecurityUpdateVersion[1]):
                uptodate_version = 1

    # if the system has an up to date update and version then it should be secure
    # if there is an older version of the update then prompt user to update
    # if none then prompt user to update OS.
    if uptodate_update == 1 and uptodate_version == 1:
        print("Your system is secure from most Vault 7 mac OS X vulnerabilties")
    elif uptodate_version == 0:
        print("Please apply the newest version of the security update to your machine")
    else:
        print("Please update OS to newest version")


"""
*Windows*
AngelFire (Xp/7), Dumbo (x32 XP/Vista/new versions), BothanSpy, Elsa, Brutal Kangaroo,
Pandemic, Athena (XP and up), AfterMidnight, Grasshopper

get list of updates
see ps script

check for missing updates
- get list o updates for Vault 7

output names of missing updates
"""
# AngelFire (Xp/7), Dumbo (x32 XP/Vista/new versions), BothanSpy(all), Elsa (all)
# Brutal Kangaroo(XP), Pandemic(all), Athena (XP and up), AfterMidnight(all)
# Grasshopper(>=8/all)


def WindowsScanner():

    path = os.popen('cd').read()
    path = path.rstrip('\n')

# Application Checker
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------

    print("Windows Application Scanner")

    # exec script in PS with path given
    full_path = ''.join(['Powershell.exe .\Windows\getappversions.ps1 ', path, '\Windows\AppVersions.txt'])

    os.system(full_path)

    # get patched versions of apps from file
    patched_versions = [patched_versions.rstrip('\n').split(': ') for patched_versions in open('Windows\Patched_versions.txt')]

    # get all apps listed in vault 7 thing
    vulnerable_apps = [vulnerable_apps.rstrip('\n') for vulnerable_apps in open('Windows\\vulnerable_apps.txt')]

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
    # get system info
    system_output = os.popen('systeminfo | findstr /B /C:"OS Name" /C:"OS Version" /C:"System Type"').read()
    print("System Information")
    print(system_output)

    # parse system info into a list
    output_split = system_output.split('\n')
    os_info = []

    for elem in output_split:
        if elem != '':
            temp = elem.split(': ')
            os_info.append(temp)

    # store parsed info into variables
    os_name = os_info[0][1].strip()
    os_build_info = os_info[1][1].strip().split(' ')
    os_ver = os_build_info[0]
    os_type = os_info[2][1].strip()

    for i in range(0, len(os_type)):
        if os_type[i].isdigit():
            os_type = os_type[i] + os_type[i+1]
            break

    # list of Windows OS's most affected by Vault 7 exploits
    affected_os = ['XP', 'Vista', '7', '8']
    status = ''

    # reconsider this block of code?
    for op_sys in affected_os:
        if op_sys in os_name:
            status = 'Please update your system to the newest version of Windows. You are vulnerable to some Vault 7 exploits. '
        else:
            status = 'Your system is not vulnerable to Vault 7 exploits.'
    print(status)

    # create full command to run PS script to retrieve a list of installed updates
    full_path = ''.join(['Powershell.exe .\Windows\getupdates.ps1 ', path, '\Windows\InstalledUpdates.txt'])

    # run above PS script
    os.system(full_path)

    # store list of installed updates into a list
    contents = [contents.rstrip('\n') for contents in open('Windows\InstalledUpdates.txt')]

    update_names = []

    for line in contents:
        if 'Title' in line:
            update_names.append(line.strip())

    # init variable to hold path to critical updates for a specific OS.
    critical_updates_file = 'Windows/'

    # determine OS and combine strings
    if 'Vista' in os_name:
        critical_updates_file = critical_updates_file + 'winVistaupdates.txt'
    elif '7' in os_name:
        critical_updates_file = critical_updates_file + 'win7updates.txt'
    elif '8' in os_name:
        critical_updates_file = critical_updates_file + 'win8updates.txt'
    else:
        critical_updates_file = critical_updates_file + 'nothing.txt'

    # store critical system updates into a list
    critical_updates = [critical_updates.rstrip('\n') for critical_updates in open(critical_updates_file)]

    # separate update name and number, then check if update applys to machine (32/64), if update num is installed updates txt file

    crit_updates = []

    for elem in critical_updates:
        temp = elem.split(': ')
        crit_updates.append(temp)

    # print(update_names)
    # print(crit_updates)

    confirmed_updates = []

    # determine which updates are installed onto machine
    for elem in crit_updates:
        if os_type in elem[0]:
            for installed_update in update_names:
                if elem[1] in installed_update:
                    confirmed_updates.append(elem[1])

    # output results
    for elem in crit_updates:
        for elem2 in confirmed_updates:
            if os_type in elem[0]:
                if elem2 in elem[1]:
                    print('Update {} is installed'.format(elem2))
                else:
                    print('Please install the following update: {} {}'.format(elem[0], elem[1]))


def main():
    system_os = platform.system()

    if system_os == 'Darwin':  # Mac
        MacScanner()
    elif system_os == 'Windows':  # Windows
        WindowsScanner()


if __name__ == "__main__":
    main()
