def collide(obj_1, obj_2):
    offset_x = obj_2.x -obj_1.x
    offset_y = obj_1.y - obj_2.y
    return obj_1.mask.overlap(obj_2.mask, (offset_x, offset_y)) != None