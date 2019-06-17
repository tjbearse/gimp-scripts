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
            # I don't think this is needed actually
            # due to layer size finding and resizing done in tileAndFlatten
            # pdb.plug_in_autocrop(img, img.layers[0])
            pass
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
            pdb.gimp_display_new(i) # TODO remove after export
    except Exception, e:
        pdb.gimp_message("an exception occured: {}".format(e))
        for i in imgs:
            pdb.gimp_image_delete(i)
    except:
        pdb.gimp_message("an exception occured")
        for i in imgs:
            pdb.gimp_image_delete(i)

def tileAndFlatten(img):
    disabled = pdb.gimp_image_undo_disable(img)
    w,h = 0,0
    padd=10
    cols, rows = findFactor(len(img.layers))
    # pdb.gimp_message("selected {},{} for {} items".format(cols, rows, len(img.layers)))

    for l in img.layers:
        if l.width > w:
            w = l.width
        if l.height > h:
            h = l.height
    imgW = w*cols + padd * (cols-1)
    imgH = h*rows + padd * (rows-1)
    pdb.gimp_image_resize(img, imgW, imgH, 0, 0)
    # reversing makes the numbers match up with sort orders
    for i, l in enumerate(reversed(img.layers)):
        col = i % cols
        row = math.floor(i / cols)
        # pdb.gimp_message("moving {} to {},{}".format(l.name, col, row))
        x = (w + padd)*col
        y = (h + padd)*row
        pdb.gimp_layer_set_offsets(l, x, y)
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
        flattenGroup(img, group)
        return []
    pdb.gimp_message("recurse into {}".format(group.name))
    imgs = []
    for layer in group.children:
        if(pdb.gimp_item_is_group(layer)):
            imgs.extend(processGroup(img, layer))
        else:
            processLayer(img, layer)
    
    if not ("[Keep]" in group.name):
        # for some reason groups can't be cut but they can be copied
        copy = pdb.gimp_edit_copy(group)
        img.remove_layer(group)
        if copy:
            newImg = pdb.gimp_edit_paste_as_new_image()
            # pdb.gimp_display_new(newImg)
            imgs.append(newImg)
    return imgs

def flattenGroup(img, group):
    # make a new layer and flatten the group onto that
    p = group.parent
    children =[]
    if not p:
        children = img.layers
    else:
        children = p.children
    i = children.index(group)
    newLayer = gimp.Layer(img, group.name+"-merged", img.width, img.height, RGB_IMAGE, 100, NORMAL_MODE)
    pdb.gimp_image_insert_layer(img, newLayer, p, i+1)
    newLayer = pdb.gimp_image_merge_down(img, group, 0)
    processLayer(img, newLayer)


def processLayer(img, layer):
    if not layer.visible:
        img.remove_layer(layer)
        return
    pdb.gimp_layer_set_offsets(layer, 0, 0)
    # auto crop works on the active layer
    pdb.gimp_image_set_active_layer(img, layer)
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
