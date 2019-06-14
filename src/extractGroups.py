#!/usr/bin/env python

from gimpfu import *

def splitGroups(img, tdrawable):
    width = img.width
    height = img.height

    order = 0
    for layer in img.layers:
        if(pdb.gimp_item_is_group(layer)):
            pdb.gimp_edit_copy(layer)
            newImg = pdb.gimp_edit_paste_as_new_image()
            pdb.gimp_display_new(newImg)

register(
        "python_fu_extract_groups",
        "Moves top level groups to new images",
        "Moves top level groups to new images",
        "TJ",
        "TJ",
        "2019",
        "<Image>/Filters/TJ/_Extract Groups",
        "RGB*, GRAY*",
        [],
        [],
        splitGroups)

main()
