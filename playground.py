
def is_number(s):

    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


def test():

    patched_versions = [patched_versions.rstrip('\n') for patched_versions in open('Windows/Patched_versions.txt')]

    pv = []

    # load info into a double thingy
    for elem in patched_versions:
        pv.append(elem.split(': '))

    app_contents = [app_contents.rstrip('\n') for app_contents in open('Windows/AppVersions.txt')] # open('Windows\AppVersions.txt')]

    app_info = []
    temp = ''
    v_start = 0
    dab = []

    # remove empty elements in list and remove excess whitespace
    for line in app_contents:
        if line != '':
            app_info.append(' '.join(line.split()))

    # separate version # and app name
    for line in app_info:
        for i in range(1, len(line)):
            if line[-i] == ' ':
                v_start = len(line) - i
                dab.append([line[0:v_start], line[v_start:len(line)].strip()])
                break

    iver = ''
    pver = ''

    for installed_app in dab:
        for patched_app in pv:
            #print('{} {}'.format(installed_app[1], patched_app[1]))
            if patched_app[0] == installed_app[0]:
                #print("its a match! {} {}".format(patched_app[0], installed_app[0]))
                iver = installed_app[1]
                pver = patched_app[1]
                print('{} {}'.format(iver, pver))

                iver = iver.split('.')
                pver = pver.split('.')
                print('{} {}'.format(iver[0], pver[0]))

                if int(iver[0]) >= int(pver[0]):
                    print("Outdated application. Please update")

    #print(dab)


def main():
    test()


if __name__ == '__main__':
    main()
