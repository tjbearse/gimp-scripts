#!/usr/bin/env python

from gimpfu import *

def collapseLayers(img, tdrawable):

    # copy to new image

    # flatten layer groups
    order = 0
    for layer in img.layers:
        if(pdb.gimp_item_is_group(layer)):
            order = extractGroup(img, layer, order)
        order += 1
    # move to top left
    # run combine/fuse

def extractGroup(img, group, order):
    for layer in group.children:
        if(pdb.gimp_item_is_group(layer)):
            order = extractGroup(img, layer, order)
        else:
            pdb.gimp_image_reorder_item(img, layer, None, order)
        order += 1
    img.remove_layer(group)
    return order


register(
        "python_fu_explode_groups",
        "Makes all groups flat",
        "Makes all groups flat",
        "TJ",
        "TJ",
        "2019",
        "<Image>/Filters/TJ/_Explode Groups",
        "RGB*, GRAY*",
        [],
        [],
        collapseLayers)

main()
