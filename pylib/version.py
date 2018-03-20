def version_to_int(version):
    l = version.split('.')
    l.extend(['0', '0', '0'])
    return int('{:0>2}{:0>2}{:0>2}'.format(*l[:3]))


def compare_version(version1, version2):
    version1, version2 = version_to_int(version1), version_to_int(version2)
    if version1 > version2:
        return 1
    elif version1 < version2:
        return -1
    else:
        return 0
