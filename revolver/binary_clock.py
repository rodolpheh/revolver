from .revolver import Revolver
from collections import namedtuple


def time_to_binary(revolver_datetime):
    """Convert a revolver object to a tuple of binary flags list

    For instance a decimal time of 9:53 would be converted to :
    .. code-block:: python
    (
        # 0b0111 == 9
        [False, True, True, True],
        # 0b0101 == 5
        [False, True, False, True],
        # 0b0011 == 3
        [False, False, True, True],
    )

    """
    # Split minutes in tens and units
    minutes = [
        int(el) for el in list('{:02d}'.format(revolver_datetime.minute))
    ]
    return (
        ['1' == el for el in list('{:04b}'.format(revolver_datetime.hour))],
        ['1' == el for el in list('{:04b}'.format(int(minutes[0])))],
        ['1' == el for el in list('{:04b}'.format(int(minutes[1])))]
    )

def ansi_clock(rev_datetime):
    """Build an ANSI representation of revolver date and time

    Date is outputted as :
    <Weekday name> <Revolutionary Day>/< Revolutionary Month>/<Holocene Year>

    Time is outputted as a binary clock
    (and a decimal representation for weaklings)
    """
    to_export = '{} {}/{}/{}\n\n'.format(
        rev_datetime.day_of_the_week,
        rev_datetime.day,
        rev_datetime.month,
        rev_datetime.year
    )

    bintuple = time_to_binary(rev_datetime)

    for i in range(4):
        to_export += '{}   {} {}\n'.format(
            '•' if bintuple[0][i] else '⁃',
            '•' if bintuple[1][i] else '⁃',
            '•' if bintuple[2][i] else '⁃'
        )

    to_export += '\n{} : {: 3d}\n'.format(
        rev_datetime.hour, rev_datetime.minute
    )
    return to_export
