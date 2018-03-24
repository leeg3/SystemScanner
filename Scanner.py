"""
Author: Greg Lee
Date: 3/24/18
Class: Scripting for Cyber Security
Purpose: System vulnerability scanner for Mac/Windows
"""

"""
notes:
steps for script:
get list o updates
check to see if certain critical updates are missing
then output names of missing updates
prompt for script to automatically install it?
done

*MAC*

get list o updates
- NAH use this: /usr/sbin/system_profiler SPInstallHistoryDataType
- this works too kinda softwareupdate -l

check to see if certain critical updates are missing


then output names of missing updates

prompt for script to automatically install it?
- sudo softwareupdate -i <name of update>
done


"""


def main():
    name = ""

if __name__ == "__main__":
    main()
