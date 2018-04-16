#!/usr/bin/env python3

from PIL import Image, ImageFont, ImageDraw

base_fields = ["x", "y", "chain", "segid", "seqpos", "name"]
def base_info_of(line):
    """
    Line format:
       x        y        chain    segid    seqpos   name
    205.500 -150.750        C       AB      0       L14
    """
    return dict(zip(base_fields, line.strip().split()))

def test_by_drawing_nt_names(im, residuewise_info):
    draw = ImageDraw.Draw(im)

    font = ImageFont.truetype("DejaVuSans.ttf", 15)

    # Pillow expects the upper left corner of the character; Matlab outputs the center

    for info in residuewise_info:
        #print(info)
        draw.text((float(info["x"])-5, float(info["y"])-5), info["name"], font=font, fill=(0,0,0,255))

    im.save("modified2.png")

def add_annotations(im, residuewise_info, annotations_fn):
    fields = ["human_name", "start_res", "end_res", "worked"]
    def annotation_info_of(line):
        return dict(zip(fields, line.strip().split()))

    def color_of(s):
        if s == "Y": return (0,255,0,255)
        else: return (255,0,0,255)

    def xy_of(ann, residuewise_info):
        """
        How to calculate the position for an annotation as a function of the loop?
        1. Just 'near the base pair where the cut happens'
        2. Involve the loop in your decision
        3. _______
        """

        # Strategy: 'off to the side' by extending the start -> end vector
        xy_end, xy_start = None, None
        for ri in residuewise_info:
            if ri["seqpos"] == ann["end_res"]:
                xy_end = (float(ri["x"]), float(ri["y"]))
            if ri["seqpos"] == ann["start_res"]:
                xy_start = (float(ri["x"]), float(ri["y"]))
            if xy_start is not None and xy_end is not None: break
        
        return ((xy_end[0]-xy_start[0])*2+xy_start[0], (xy_end[1]-xy_start[1])*2+xy_start[1])

    annotations = []
    with open(annotations_fn) as f:
        annotations = [annotation_info_of(l) for l in f.readlines()]

    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("DejaVuSans.ttf", 15)
    
    def draw_text_with_box(draw, font, text, fill, location):
        text_size = font.getsize(text)
        draw.rectangle(((location[0]-5, location[1]-5), (location[0]+text_size[0]+5, location[1]+text_size[1]+5)), fill='white', outline=fill)
        draw.text(location, text, font=font, fill=fill)

    def draw_line_between(draw, pt1, pt2, worked, info):
        """
        Note that we have to connect 'residue before start' with 'residue
        after end'.
        """

        xy_end, xy_start = None, None
        for ri in residuewise_info:
            if int(ri["seqpos"]) == int(pt1)-1:
                print(int(ri["seqpos"]))
                xy_start = (float(ri["x"]), float(ri["y"]))
            if int(ri["seqpos"]) == int(pt2)+1:
                print(int(ri["seqpos"]))
                xy_end = (float(ri["x"]), float(ri["y"]))
            if xy_start is not None and xy_end is not None: break
            
        draw.line((xy_start[0], xy_start[1], xy_end[0], xy_end[1]), fill=color_of(worked), width=5)

    for ann in annotations:
        print("Ann:", ann)
        draw_text_with_box(draw, font, ann["human_name"], color_of(ann["worked"]), xy_of(ann, residuewise_info))
        draw_line_between(draw, ann["start_res"], ann["end_res"], ann["worked"], residuewise_info)

    im.save("annotated.png")



if __name__ == "__main__":
    im = Image.open("drawing_new.png")
    
    residuewise_info = []
    with open("drawing.png.coords.txt") as f:
        for line in f.readlines():
            residuewise_info.append(base_info_of(line))
    
    add_annotations(im, residuewise_info, "annotations.txt")

