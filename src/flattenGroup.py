#!/usr/bin/env python
# TODO
exit()

from gimpfu import *

def flattenGroup(img, group):
    frozen = pdb.gimp_image_freeze_layers(img)
    disabled = pdb.gimp_image_undo_disable(img)
    try:
        pass
        # get parent and order
        # new layer right above me
        gimp
        # merge down
        layer = pdb.gimp_image_merge_down(image, merge_layer, merge_type)
    finally:
        if frozen:
            pdb.gimp_image_thaw_layers(img)
        if disabled:
            pdb.gimp_image_undo_enable(img)

def collapseLayers(img, tdrawable):
    pdb.gimp_image_freeze_layers(img)
    try:
        order = 0
        for layer in img.layers:
            if(pdb.gimp_item_is_group(layer)):
                order = extractGroup(img, layer, order)
            order += 1
    finally:
        pdb.gimp_image_thaw_layers(img)

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
