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
# check to make sure no VLC ver: 2.1.5, Notepad++ no 7.3.2 and Earlier, chrome newer than 55.0.2883

def MacScanner():
    # get updates from system
    minVersion = "10.20"
    """ CHANGE BACK TO 10.10 """
    minSecurityUpdateVersion = [2017, 3] #OG 2015, 6

    print("Mac Scanner")

    affected_programs = [['VLC\\ Media\\ Player.app', ''],
    ['Irfan\\ View.app', ''], ['Google\\ Chrome.app',''],
    ['Opera.app', ''], ['Firefox.app',''], ['Thunderbird.app',''],
    ['Opera\\ Mail.app',''], ['Foxit\\ Reader.app',''],
    ['Libre\\ Office.app',''], ['Notepad++.app',''],
    ['Skype.app',''], ['7-Zip.app',''], ['ClamWin.app',''],
    ['Kasperksy\\ TDSS\\ Killer.app',''], ['McAfee\\ Stinger.app',''], ['Sophos\\ Virus\\ Removal.app',''], ['Prezi.app',''],
    ['Babel\\ Pad.app',''], ['Iperius\\ Backup.app',''],
    ['Sandisk\\ Secure',''], ['U3\\ Software.app',''], ['2048.app',''],
    ['LBreakout2.app''']]

    print(len(affected_programs))

    print(affected_programs[0][0], affected_programs[0][1])
    commands= []
    for ap in affected_programs:
        commands.append(''.join(['mdls /Applications/', ap[0], ' -name kMDItemVersion | awk -F \'\"\' \'{print $2}\'']))

    print(len(commands))
    for i in range(0, len(affected_programs)-1):
        affected_programs[i][1] = os.popen(commands[i]).read().rstrip('\n')

    print(affected_programs)


#----------------------------------------------------------------------------
    os.system("defaults read loginwindow SystemVersionStampAsString > SystemVersion.txt")

    # check system OS. if older than 10.10 then proceed with updates check
    print("Getting System OS version")
    OS_version = [OS_version.rstrip('\n') for OS_version in open('SystemVersion.txt')]

    temp = OS_version[0].split('.')
    temp2 = minVersion.split('.')

    if int(temp[1]) > int(temp2[1]):
        print("OS is good")
        return
    else:
        print("OS is subject to vulnerabilities")

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
    for i in range(0, len(update_names)):
        # print(update_names[i])
        update_version_num.append(update_names[i].split(' '))

    # print(num)
    # print(update_names)
    # get individual number, see how it compares to minSecurityUpdateVersion
    # print(update_version_num[0][2])
    uptodate_update = 0
    uptodate_version = 0

    for value in update_version_num:
        temp = value[2].split('-')
        # print("{} {}".format(temp[0], temp[1]))

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


# AngelFire (Xp/7), Dumbo (x32 XP/Vista/new versions), BothanSpy, Elsa, Brutal Kangaroo,
# Pandemic, Athena (XP and up), AfterMidnight, Grasshopper
# DONT FORGET CHECKING APP VERSIONS
# check to make sure no VLC ver: 2.1.5, Notepad++ no 7.3.2 and Earlier, chrome newer than 55.0.2883
#
""" all affected app versions, not all have patched it bc things
VLC Media Player, Irfan View, Chrome, Opera, Firefox, Thunderbird, Opera Mail, Foxit Reader, Libre Office, Notepad++, Skype, 7-Zip, ClamWin, Kasperksy TDSS Killer, McAfee Stinger, Sophos Virus Removal, Prezi, Babel Pad, Iperius Backup, Sandisk Secure, U3 Software, 2048, LBreakout2
"""

def WindowsScanner():
    print("Windows Scanner")
    os_info = os.popen('systeminfo | findstr /B /C:"OS Name" /C:"OS Version"').read()
    os_name = os_info[0].rstrip('\n')
    os_ver = os_info[1].rstrip('\n')

    path = os.popen('cd').read()
    path = path.rstrip('\n')

    # exec script in PS with path given
    full_path = ''.join(['Powershell.exe .\Windows\getappversions.ps1 ', path, '\Windows\AppVersions.txt'])

# Application Checker
# ---------------------------------------------------------------------------------------

    print("Checking installed applications")
    os.system(full_path)

    app_contents = [app_contents.rstrip('\n') for app_contents in open('Windows\AppVersions.txt')]

    print(app_contents)
    app_info = []

    for line in app_contents:
        if line != '':
            for i in range(0, len(line)):
                if line[i].isdigit():
                    line[i-1].replace(' ', ' :')
            app_info.append(' '.join(line.split()))

    print(app_info)

    temp = "Hello 123"
    print(temp[2])

# System Checker
# ---------------------------------------------------------------------------------------

    print("Checking System")

    print(os_info)

    if 'XP, Vista, 7, 8' in os_name:
        print('YOU GONNA ESPLODE')
    else:
        print('your ok')

    # exec script in PS with path given
    full_path = ''.join(['Powershell.exe .\Windows\getupdates.ps1 ', path, '\Windows\InstalledUpdates.txt'])

    # run PS script to get updates and put into file
    os.system(full_path)

    contents = [contents.rstrip('\n') for contents in open('Windows\InstalledUpdates.txt')]
    print(contents)

    filtered_contents = []

    for line in contents:
        if 'Succeeded' in line or 'Title' in line:
            filtered_contents.append(line.strip())

    print(filtered_contents)


# def LinuxScanner():
#     print("Linux Scanner")


def main():
    system_os = platform.system()

    if system_os == 'Darwin':  # Mac
        MacScanner()
    elif system_os == 'Windows':  # Windows
        WindowsScanner()
#    else: #Linux
#        LinuxScanner()


if __name__ == "__main__":
    main()
