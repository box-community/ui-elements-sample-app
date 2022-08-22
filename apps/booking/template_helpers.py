"""
functions to help with templates
"""

from apps.booking.utils import get_all_dive_sites


def get_all_dive_sites_options():
    """
    Return a list of tuples with the dive site id and name.
    """

    mylist = get_all_dive_sites()

    options = []
    for row in mylist:
        options.append((row.id, row.name))

    options.insert(0, ('', 'Select a dive site'))

    return options



