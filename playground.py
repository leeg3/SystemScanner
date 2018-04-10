
def test():

    patched_versions = [patched_versions.rstrip('\n').split(': ') for patched_versions in open('Windows/Patched_versions.txt')]

    app_contents = [app_contents.rstrip('\n') for app_contents in open('Windows/AppVersions.txt')] # open('Windows\AppVersions.txt')]

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

    for installed_app in app_sorted:
        for patched_app in patched_versions:
            if patched_app[0] == installed_app[0]:

                iver = installed_app[1].split('.')
                pver = patched_app[1].split('.')

                if int(iver[0]) >= int(pver[0]):
                    print("{} is outdated. Please update".format(installed_app[0]))


def main():
    test()


if __name__ == '__main__':
    main()




"""
    # remove empty elements in list and remove excess whitespace
    for line in app_contents:
        if line != '':
            app_info.append(' '.join(line.split()))

    # separate version # and app name
    for line in app_info:
        for i in range(1, len(line)):
            if line[-i] == ' ':
                v_start = len(line) - i
                dab.append([line[0:v_start], line[v_start+1:len(line)]])
                break


if int(temp[0]) > minSecurityUpdateVersion[0]:
    # print("its a new security update")
    uptodate_update = 1
elif int(temp[0]) == int(minSecurityUpdateVersion[0]):
    if int(temp[1]) > int(minSecurityUpdateVersion[1]):
        # print("its a new security version")
        uptodate_version = 1
"""
