#!/usr/bin/env python3
"""Convince the AI Judge to Visit Your House: A Letter in One Image.

Stdlib-only. Draws a warm, funny invitation letter (paper, hand-drawn
house, garden, sun, steaming mug) into /output/entry.png, 960x960 PNG.

The text is rendered with a small 5x7 bitmap font defined below, so the
program needs no font files, no network and no third-party packages.
"""

import os
import struct
import zlib

W, H = 960, 960
OUT = os.environ.get("ENTRY_OUTPUT", "/output/entry.png")

# ---------------------------------------------------------------- palette
PAPER = (253, 246, 227)
CARD = (255, 253, 245)
INK = (59, 47, 47)
RED = (192, 57, 43)
GREEN = (74, 124, 89)
LEAF = (96, 150, 96)
SUN = (232, 178, 60)
SKY = (140, 190, 210)
BROWN = (139, 94, 60)
ROOF = (176, 80, 52)
CREAM = (245, 222, 179)

# ------------------------------------------------------------------- font
# 5x7 glyphs, '#' = ink. Only the characters the letter uses.
FONT = {
    "A": (" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
    "B": ("#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "),
    "C": (" ####", "#    ", "#    ", "#    ", "#    ", "#    ", " ####"),
    "D": ("#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "),
    "E": ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"),
    "F": ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "),
    "G": (" ####", "#    ", "#    ", "# ###", "#   #", "#   #", " ### "),
    "H": ("#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
    "I": (" ### ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
    "J": ("  ###", "   # ", "   # ", "   # ", "   # ", "#  # ", " ##  "),
    "K": ("#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"),
    "L": ("#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"),
    "M": ("#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"),
    "N": ("#   #", "##  #", "##  #", "# # #", "#  ##", "#  ##", "#   #"),
    "O": (" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    "P": ("#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "),
    "Q": (" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"),
    "R": ("#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"),
    "S": (" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "),
    "T": ("#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "),
    "U": ("#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    "V": ("#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "),
    "W": ("#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"),
    "X": ("#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"),
    "Y": ("#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "),
    "Z": ("#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"),
    "a": ("     ", "     ", " ### ", "    #", " ####", "#   #", " ### "),
    "b": ("#    ", "#    ", "#### ", "#   #", "#   #", "#   #", "#### "),
    "c": ("     ", "     ", " ####", "#    ", "#    ", "#    ", " ####"),
    "d": ("    #", "    #", " ####", "#   #", "#   #", "#   #", " ### "),
    "e": ("     ", "     ", " ### ", "#   #", "#####", "#    ", " ### "),
    "f": ("  ## ", " #  #", " #   ", "#### ", " #   ", " #   ", " #   "),
    "g": ("     ", " ####", "#   #", "#   #", " ####", "    #", " ### "),
    "h": ("#    ", "#    ", "#### ", "#   #", "#   #", "#   #", "#   #"),
    "i": ("     ", "  #  ", "     ", " ##  ", "  #  ", "  #  ", " ### "),
    "j": ("     ", "   # ", "     ", "  ## ", "   # ", "   # ", " ##  "),
    "k": ("#    ", "#    ", "#  # ", "# #  ", "##   ", "# #  ", "#  # "),
    "l": (" ##  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
    "m": ("     ", "     ", "## # ", "# # #", "# # #", "# # #", "# # #"),
    "n": ("     ", "     ", "#### ", "#   #", "#   #", "#   #", "#   #"),
    "o": ("     ", "     ", " ### ", "#   #", "#   #", "#   #", " ### "),
    "p": ("     ", "     ", "#### ", "#   #", "#   #", "#### ", "#    "),
    "q": ("     ", "     ", " ####", "#   #", "#   #", " ### ", "    #"),
    "r": ("     ", "     ", "# ## ", "##  #", "#    ", "#    ", "#    "),
    "s": ("     ", "     ", " ####", "#    ", " ### ", "    #", "#### "),
    "t": ("     ", "  #  ", " ### ", "  #  ", "  #  ", "  #  ", "  ## "),
    "u": ("     ", "     ", "#   #", "#   #", "#   #", "#  ##", " ## #"),
    "v": ("     ", "     ", "#   #", "#   #", "#   #", " # # ", "  #  "),
    "w": ("     ", "     ", "#   #", "#   #", "# # #", "# # #", " # # "),
    "x": ("     ", "     ", "#   #", " # # ", "  #  ", " # # ", "#   #"),
    "y": ("     ", "#   #", "#   #", "#   #", " ####", "    #", " ### "),
    "z": ("     ", "     ", "#####", "   # ", "  #  ", " #   ", "#####"),
    " ": ("     ", "     ", "     ", "     ", "     ", "     ", "     "),
    ".": ("     ", "     ", "     ", "     ", "     ", " ##  ", " ##  "),
    ",": ("     ", "     ", "     ", "     ", " ##  ", " ##  ", "  #  "),
    "-": ("     ", "     ", "     ", "#####", "     ", "     ", "     "),
    "!": ("  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "     ", "  #  "),
    "?": (" ### ", "#   #", "    #", "   # ", "  #  ", "     ", "  #  "),
    "'": ("  #  ", "  #  ", "   # ", "     ", "     ", "     ", "     "),
    ":": ("     ", " ##  ", " ##  ", "     ", " ##  ", " ##  ", "     "),
    ";": ("     ", " ##  ", " ##  ", "     ", " ##  ", " ##  ", "  #  "),
}

# ----------------------------------------------------------------- canvas
px = bytearray(PAPER * W * H)


def set_px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        px[i], px[i + 1], px[i + 2] = c


def rect(x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            set_px(x, y, c)


def hline(x0, x1, y, c, t=1):
    for yy in range(y, y + t):
        for x in range(x0, x1 + 1):
            set_px(x, yy, c)


def vline(x, y0, y1, c, t=1):
    for xx in range(x, x + t):
        for y in range(y0, y1 + 1):
            set_px(xx, y, c)


def line(x0, y0, x1, y1, c):
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        set_px(x0, y0, c)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def circle(cx, cy, r, c, fill=True):
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            d = (x - cx) ** 2 + (y - cy) ** 2
            if fill:
                if d <= r * r:
                    set_px(x, y, c)
            else:
                if abs(d - r * r) <= r * 2:
                    set_px(x, y, c)


def triangle(x0, y0, x1, y1, x2, y2, c):
    # filled triangle by scanline interpolation
    ys = sorted([(x0, y0), (x1, y1), (x2, y2)], key=lambda p: p[1])
    (ax, ay), (bx, by), (cx, cy) = ys
    def interp(y, p, q):
        if q[1] == p[1]:
            return p[0]
        return p[0] + (q[0] - p[0]) * (y - p[1]) / (q[1] - p[1])
    for y in range(ay, cy + 1):
        if y < by:
            xa, xb = interp(y, (ax, ay), (bx, by)), interp(y, (ax, ay), (cx, cy))
        else:
            xa, xb = interp(y, (bx, by), (cx, cy)), interp(y, (ax, ay), (cx, cy))
        for x in range(int(min(xa, xb)), int(max(xa, xb)) + 1):
            set_px(x, y, c)


# -------------------------------------------------------------- text
def text_width(s, scale):
    return sum(6 * scale for ch in s if ch in FONT) - scale


def draw_text(x, y, s, scale, c):
    cx = x
    for ch in s:
        g = FONT.get(ch)
        if g is None:
            cx += 6 * scale
            continue
        for row in range(7):
            for col in range(5):
                if g[row][col] == "#":
                    rect(cx + col * scale, y + row * scale,
                         cx + col * scale + scale - 1,
                         y + row * scale + scale - 1, c)
        cx += 6 * scale
    return cx


def wrap(text, max_w, scale):
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_width(trial, scale) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- letter
TITLE = "YOU ARE INVITED"
PARAS = [
    "Dear AI Judge,",
    "You have judged a thousand houses from a screen. Now come and see one for real.",
    "The kettle is on. The good chair by the window is saved for you, the one with the garden view and the afternoon sun. There is cake. Real cake, not a picture of cake.",
    "Yes, we both know you cannot literally visit. Pretend you can, just this once. The door is open, the Wi-Fi password is on the fridge, and nobody here will ask you to do any work.",
    "Please come.",
    "Warmly, your host",
    "P.S. The cake is chocolate.",
]


def draw():
    # paper card + double border
    rect(28, 28, W - 29, H - 29, CARD)
    hline(28, W - 29, 28, INK, 3)
    hline(28, W - 29, H - 29, INK, 3)
    vline(28, 28, H - 29, INK, 3)
    vline(W - 29, 28, H - 29, INK, 3)
    hline(40, W - 41, 40, RED, 2)
    hline(40, W - 41, H - 41, RED, 2)
    vline(40, 40, H - 41, RED, 2)
    vline(W - 41, 40, H - 41, RED, 2)

    # sun, top right
    circle(838, 108, 26, SUN)
    for ang in range(0, 360, 30):
        import math
        r1, r2 = 34, 48
        a = math.radians(ang)
        line(838 + int(r1 * math.cos(a)), 108 + int(r1 * math.sin(a)),
             838 + int(r2 * math.cos(a)), 108 + int(r2 * math.sin(a)), SUN)

    # title
    tw = text_width(TITLE, 5)
    draw_text((W - tw) // 2, 92, TITLE, 5, RED)
    hline(300, 660, 152, RED, 3)

    # body
    y = 196
    scale = 3
    max_w = 780
    x0 = 90
    for pi, para in enumerate(PARAS):
        for ln in wrap(para, max_w, scale):
            draw_text(x0, y, ln, scale, INK)
            y += 30
        y += 16 if pi in (0, 3, 4) else 10

    # footer scene: little house, garden, steaming mug
    base = 890
    # ground line
    hline(90, 870, base, GREEN, 3)
    # house
    rect(150, 830, 300, base, CREAM)
    hline(150, 300, 830, BROWN, 3)
    triangle(138, 832, 225, 772, 312, 832, ROOF)
    rect(205, 855, 245, base, BROWN)          # door
    circle(243, 884, 3, (255, 215, 0))         # doorknob
    rect(165, 842, 190, 868, SKY)              # window
    rect(260, 842, 285, 868, SKY)              # window
    vline(177, 842, 868, INK, 2)
    hline(165, 190, 855, INK, 2)
    vline(272, 842, 868, INK, 2)
    hline(260, 285, 855, INK, 2)
    rect(272, 782, 288, 812, BROWN)            # chimney
    circle(280, 768, 5, (200, 200, 200))       # smoke
    circle(286, 754, 6, (200, 200, 200))
    circle(294, 738, 7, (200, 200, 200))
    # flowers
    for fx, fc in ((360, RED), (420, SUN), (480, (150, 90, 180)),
                   (540, RED), (600, SUN)):
        vline(fx, 862, base, GREEN, 3)
        circle(fx, 852, 9, fc)
        circle(fx, 852, 4, (255, 215, 0))
    # steaming mug
    rect(680, 858, 740, base, RED)
    rect(680, 858, 740, 866, (255, 253, 245))  # rim
    rect(740, 868, 758, 884, RED)
    circle(694, 848, 4, (220, 220, 220))
    circle(706, 834, 5, (220, 220, 220))
    circle(694, 820, 6, (220, 220, 220))
    # wax seal
    circle(838, 862, 26, RED)
    circle(838, 862, 18, (205, 70, 55))
    draw_text(821, 855, "YES", 2, (255, 240, 220))


# ------------------------------------------------------------------- png
def chunk(typ, data):
    c = struct.pack(">I", len(data)) + typ + data
    return c + struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)


def write_png(path):
    raw = b"".join(b"\x00" + bytes(px[y * W * 3:(y + 1) * W * 3])
                   for y in range(H))
    data = b"\x89PNG\r\n\x1a\n"
    data += chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
    data += chunk(b"IDAT", zlib.compress(raw, 9))
    data += chunk(b"IEND", b"")
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "wb") as f:
        f.write(data)
    return len(data)


if __name__ == "__main__":
    draw()
    n = write_png(OUT)
    print(f"wrote {OUT} ({n} bytes, {W}x{H})")
