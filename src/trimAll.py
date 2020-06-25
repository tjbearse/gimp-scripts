#!/usr/bin/env python

from gimpfu import *

def cropLayers(img, tdrawable):
    disabled = pdb.gimp_image_undo_disable(img)
    try:
        cropLayersHelper(img, img.layers)
    except Exception, e:
        pdb.gimp_message("an exception occured: {}".format(e))
    finally:
        if disabled:
            pdb.gimp_image_undo_enable(img)

def cropLayersHelper(img, layers):
    for layer in layers:
        if(pdb.gimp_item_is_group(layer)):
            cropLayersHelper(img, layer.children)
        else:
            pdb.gimp_image_set_active_layer(img, layer)
            pdb.plug_in_autocrop_layer(img, layer)

register(
        "python_fu_crop_layers",
        "trims all layers to content",
        "trims all layers to content",
        "TJ",
        "TJ",
        "2019",
        "<Image>/Filters/TJ/_Crop All Layers",
        "RGB*, GRAY*",
        [],
        [],
        cropLayers)

main()
