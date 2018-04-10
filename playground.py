def test():

    contents = [contents.rstrip('\n') for contents in open('Windows/InstalledUpdates.txt')] #open('Windows\InstalledUpdates.txt')]

    filtered_contents = []

    # get names of each installed update
    for i in range(0,len(contents)):
        if 'Succeeded' in contents[i]:
            filtered_contents.append(contents[i+1].strip())

    print(filtered_contents)

    



def main():
    test()


if __name__ == '__main__':
    main()




"""


==================

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
