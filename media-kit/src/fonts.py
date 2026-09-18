"""TrueType copies of the installed Inter (CFF/OpenType) fonts.

Chrome embeds CFF fonts in PDFs as Type 3, which print shops flag and some
viewers render poorly. Converting the outlines to quadratic TrueType makes
Chrome embed a normal TrueType font.
"""

from pathlib import Path

from fontTools.pens.cu2quPen import Cu2QuPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.ttLib import TTFont, newTable

INTER_DIR = Path("/usr/share/fonts/opentype/inter")
WEIGHTS = {400: "Inter-Regular.otf", 600: "Inter-SemiBold.otf", 700: "Inter-Bold.otf"}


def otf_to_ttf(src, dst, max_err=1.0):
    font = TTFont(src)
    order = font.getGlyphOrder()
    glyph_set = font.getGlyphSet()
    glyf = newTable("glyf")
    glyf.glyphOrder = order
    glyf.glyphs = {}
    for name in order:
        pen = TTGlyphPen(None)
        glyph_set[name].draw(Cu2QuPen(pen, max_err, reverse_direction=True))
        glyf.glyphs[name] = pen.glyph()
    font["loca"] = newTable("loca")
    font["glyf"] = glyf
    del font["CFF "]
    if "VORG" in font:
        del font["VORG"]
    glyf.compile(font)
    hmtx = font["hmtx"]
    for name, g in glyf.glyphs.items():
        if hasattr(g, "xMin"):
            hmtx[name] = (hmtx[name][0], g.xMin)
    maxp = newTable("maxp")
    maxp.tableVersion = 0x00010000
    for attr in ("maxZones", "maxTwilightPoints", "maxStorage", "maxFunctionDefs",
                 "maxInstructionDefs", "maxStackElements", "maxSizeOfInstructions",
                 "maxComponentElements"):
        setattr(maxp, attr, 0)
    maxp.maxZones = 1
    font["maxp"] = maxp
    maxp.compile(font)
    post = font["post"]
    post.formatType = 2.0
    post.extraNames = []
    post.mapping = {}
    post.glyphOrder = order
    font["head"].indexToLocFormat = 0
    font["head"].glyphDataFormat = 0
    font.sfntVersion = "\000\001\000\000"
    font.save(dst)


def inter_font_faces(out_dir):
    """Convert once, return @font-face CSS pointing at the TrueType files."""
    out_dir.mkdir(parents=True, exist_ok=True)
    css = []
    for weight, name in WEIGHTS.items():
        dst = out_dir / name.replace(".otf", ".ttf")
        if not dst.exists():
            otf_to_ttf(INTER_DIR / name, dst)
        css.append(f"@font-face {{ font-family: Inter; font-weight: {weight}; "
                   f"src: url('{dst.as_uri()}') format('truetype') }}")
    return "\n".join(css)
