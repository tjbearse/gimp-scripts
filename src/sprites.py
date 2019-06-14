#!/usr/bin/env python

from gimpfu import *
import math

def sprites(img, tdrawable):
    pdb.gimp_message("starting")
    img = pdb.gimp_image_duplicate(img)
    disabled = pdb.gimp_image_undo_disable(img)
    imgs = [img]
    try:
        for layer in img.layers:
            if(pdb.gimp_item_is_group(layer)):
                imgs.extend(processGroup(img, layer))
            else:
                processLayer(img, layer)
        pdb.gimp_message("all images {}".format(",".join([i.name for i in imgs])))

        if len(img.layers) > 0:
            # others already did this with paste
            pdb.plug_in_autocrop(img, img.layers[0])
        else:
            imgs.pop(0)
            pdb.gimp_message("staring img now emtpy")
            pdb.gimp_image_delete(img)
            disabled = False
            
        for i in imgs:
            pdb.gimp_message("flattening {}".format(i.layers[0].name))
            pdb.python_fu_explode_groups(i, i.layers[0])
            tileAndFlatten(i)
            # fuse images # pdb.script_fu_fuse_layers(image, drawable, str(cols))
            # write this myself?
            # export fused images
            pdb.gimp_display_new(i) # TODO remove
    except Exception, e:
        pdb.gimp_message("an exception occured: {}".format(e))
        for i in imgs:
            pdb.gimp_image_delete(i)
    except:
        pdb.gimp_message("an exception occured")
        for i in imgs:
            pdb.gimp_image_delete(i)
    finally:
        if disabled:
            pdb.gimp_image_undo_enable(img)

def tileAndFlatten(img):
    disabled = pdb.gimp_image_undo_disable(img)
    w,h = 0,0
    cols, rows = findFactor(len(img.layers))
    # pdb.gimp_message("selected {},{} for {} items".format(cols, rows, len(img.layers)))

    for l in img.layers:
        if l.width > w:
            w = l.width
        if l.height > h:
            h = l.height
    
    pdb.gimp_image_resize(img, w*cols, h*rows, 0, 0)
    for i, l in enumerate(img.layers):
        col = i % cols
        row = math.floor(i / rows)
        # pdb.gimp_message("moving {} to {},{}".format(l.name, col, row))
        pdb.gimp_layer_set_offsets(l, w*col, h*row)
    layer = pdb.gimp_image_merge_visible_layers(img, 0) # 0 is for "expand"
    if disabled:
        pdb.gimp_image_undo_enable(img)

# find the most square combo possible
def findFactor(n):
    factor = math.ceil(math.sqrt(n))
    return factor, math.ceil(n/factor);

def processGroup(img, group):
    if not group.visible:
        img.remove_layer(group)
        return []
    elif "[Flat]" in group.name:
        # TODO merge these down using flatten group thing in file next door
        return []
        # merge down?
    elif "[Keep]" in group.name:
        # don't touch these, they'll get hit with exploder
        return []
    pdb.gimp_message("recurse into {}".format(group.name))
    imgs = []
    for layer in group.children:
        if(pdb.gimp_item_is_group(layer)):
            imgs.extend(processGroup(img, layer))
        else:
            processLayer(img, layer)
    
    # for some reason groups can't be cut but they can be copied
    copy = pdb.gimp_edit_copy(group)
    img.remove_layer(group)
    if copy:
        newImg = pdb.gimp_edit_paste_as_new_image()
        # pdb.gimp_display_new(newImg)
        imgs.append(newImg)
    return imgs

def processLayer(img, layer):
    if not layer.visible:
        img.remove_layer(layer)
        return
    pdb.gimp_layer_set_offsets(layer, 0, 0)
    pdb.plug_in_autocrop_layer(img, layer)

register(
        "python_fu_groups_to_sprites",
        "Transforms groups into sprite sheets",
        "All groups without [Flat] are extracted to new files and then made into a sprite sheet",
        "TJ",
        "TJ",
        "2019",
        "<Image>/Filters/TJ/_Sprite Groups",
        "RGB*, GRAY*",
        [],
        [],
        sprites)

main()
