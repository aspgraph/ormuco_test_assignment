# Declaring a custom exception in order to catch inner errors
class CompareFormatException(Exception):
    pass


# Alphabetic version parts: Alpha (a), Beta (b), Release Candidate (rc), Release (r)
# Alpha is preceding Beta, which is preceding RC and Release
alpha_versions = [['a', '-3'], ['b', '-2'], ['rc', '-1'], ['r', '0']]
# Saved exception text
compException = CompareFormatException('Wrong format! Both strings should be two-version non-negative integer strings.')


# Decomposing the version string into substrings divided by dots or alphabetical parts
def decompose_version(v):
    dec = v.split('.')
    if len(dec) < 1 or any(len(elem) == 0 for elem in dec):
        raise compException
    ret = []
    # Only allow one alphabetic sequence per version string
    has_alpha = False
    for str_num in dec:
        # If a string contains alphabetical parts, e.g. 1.0rc2, then 'rc' should be replaced with negative numbers
        # to precede release (which goes from 0 and up)
        for alpha, val in alpha_versions:
            if str_num[0].isdigit() and str_num.find(alpha) != -1:
                if has_alpha:
                    raise compException
                # Extracting the alphabetic parts
                sub_arr = str_num.split(alpha, 1)
                # Removing the last element from the version parts if it's empty
                if sub_arr[-1] == '':
                    sub_arr = sub_arr[:-1]
                if any(not sub.isdigit() for sub in sub_arr):
                    raise compException
                else:
                    ret.append(long(sub_arr[0]))
                    ret.append(long(val))
                    if len(sub_arr) == 2:
                        ret.append(long(sub_arr[1]))
                    has_alpha = True
                break
        else:
            # No alphabetic parts were found
            if not str_num.isdigit():
                raise compException
            else:
                ret.append(long(str_num))
    return ret


# Compare two version strings
# First, decompose the version strings into parts
def compare_versions(v1, v2):
    dv1, dv2 = [decompose_version(v) for v in [v1, v2]]
    # Next, compare the parts one-by-one
    for i in range(0, max(len(dv1), len(dv2))):
        x1, x2 = [dv[i] if i < len(dv) else 0 for dv in [dv1, dv2]]
        if x1 < x2:
            return 'Less'
        elif x1 > x2:
            return 'Greater'
    return 'Equals'
