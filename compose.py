"""THE WORLD front page: 50 stories of Thursday 19 November 2026.

Draws a dense broadsheet front page with Pillow and real DejaVu fonts:
masthead, dateline, a dot-matrix world map, five lead stories with short
decks, four small drawn icons, and 45 compact headlines in three columns
under section headers. No AI-generated text anywhere.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = (255, 255, 255)
INK = (17, 17, 17)
NAVY = (27, 58, 92)
RED = (178, 34, 34)
GREY = (85, 85, 85)
RULE = (150, 150, 150)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    """Greedy word wrap by pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if fnt.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# --- dot-matrix world map: land ranges per row, 60 cols x 22 rows ---
# (col = 6 deg longitude from -180; row = ~6 deg latitude from 75N)
MAP_ROWS = [
    [(2, 12), (20, 26), (30, 32), (37, 59)],
    [(2, 20), (21, 26), (30, 33), (37, 59)],
    [(3, 20), (22, 25), (28, 37), (37, 58)],
    [(3, 19), (28, 38), (38, 58)],
    [(4, 20), (28, 36), (38, 57)],
    [(6, 20), (28, 35), (38, 55)],
    [(7, 19), (29, 36), (38, 53)],
    [(8, 18), (27, 36), (38, 50)],
    [(9, 13), (27, 37), (40, 48)],
    [(10, 12), (27, 37), (42, 46), (47, 50)],
    [(12, 15), (27, 37), (43, 45), (47, 50)],
    [(15, 17), (18, 24), (28, 37), (48, 50)],
    [(18, 24), (28, 37), (47, 53)],
    [(18, 23), (29, 36), (48, 52)],
    [(18, 22), (30, 36), (49, 55)],
    [(19, 22), (30, 35), (49, 56)],
    [(19, 21), (30, 34), (49, 55)],
    [(19, 21), (31, 34), (50, 55)],
    [(19, 20), (31, 33), (50, 54)],
    [(19, 20), (51, 53)],
    [(19, 20)],
    [(19, 19)],
]


def draw_map(d, x0, y0, width, height):
    """Downsample the 60x22 land mask to 60x11 dots (rows merged in pairs)."""
    cols, rows = 60, 11
    px, py = width / cols, height / rows
    land = [[False] * cols for _ in range(rows)]
    for r, ranges in enumerate(MAP_ROWS):
        for a, b in ranges:
            for c in range(a, b + 1):
                land[r // 2][c] = True
    for r in range(rows):
        for c in range(cols):
            if land[r][c]:
                cx = x0 + c * px + px / 2
                cy = y0 + r * py + py / 2
                rad = 2.8
                d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad], fill=NAVY)


# --- small geometric icons (46x46 box), navy ---
def draw_tanker(d, x, y):
    d.polygon([(x + 2, y + 30), (x + 44, y + 30), (x + 38, y + 20),
               (x + 8, y + 20)], fill=NAVY)
    d.rectangle([x + 28, y + 12, x + 34, y + 20], fill=NAVY)
    d.rectangle([x + 12, y + 16, x + 24, y + 20], fill=NAVY)
    for wy in (36, 41):
        d.line([(x + 2, y + wy), (x + 14, y + wy), (x + 20, y + wy - 3),
                (x + 32, y + wy), (x + 44, y + wy)], fill=NAVY, width=2)


def draw_gavel(d, x, y):
    d.rounded_rectangle([x + 6, y + 8, x + 30, y + 18], radius=3, fill=NAVY)
    d.line([(x + 22, y + 18), (x + 34, y + 38)], fill=NAVY, width=5)
    d.line([(x + 6, y + 42), (x + 40, y + 42)], fill=NAVY, width=3)


def draw_controller(d, x, y):
    d.rounded_rectangle([x + 2, y + 14, x + 44, y + 34], radius=9, fill=NAVY)
    d.rectangle([x + 10, y + 21, x + 18, y + 27], fill=BG)
    d.rectangle([x + 12, y + 19, x + 16, y + 29], fill=BG)
    d.ellipse([x + 30, y + 20, x + 35, y + 25], fill=BG)
    d.ellipse([x + 36, y + 24, x + 41, y + 29], fill=BG)


def draw_building(d, x, y):
    d.polygon([(x + 4, y + 16), (x + 42, y + 16), (x + 23, y + 5)], fill=NAVY)
    for cx in (10, 20, 30):
        d.rectangle([x + cx, y + 19, x + cx + 4, y + 36], fill=NAVY)
    d.rectangle([x + 4, y + 38, x + 42, y + 43], fill=NAVY)


ICONS = {"tanker": draw_tanker, "gavel": draw_gavel,
         "controller": draw_controller, "building": draw_building}

# --- content ---
LEAD1_HEAD = "TRUMP, XI AND PUTIN HOLD FIRST-EVER TRILATERAL SUMMIT IN SHENZHEN"
LEAD1_DECK = ("Nuclear arms, Iran and Ukraine on the table; bilateral talks and a "
              "working lunch with Xi, one-on-one with Putin.")

GRID = [
    ("tanker",
     "IRAN SAYS THREE TANKERS HIT MINES EAST OF HORMUZ",
     "Navig8 Messi struck off Oman; 11 crew hurt, one missing."),
    ("gavel",
     "WORLD COURT RULES ON MYANMAR ROHINGYA GENOCIDE CASE",
     "Decided at the Peace Palace in The Hague."),
    ("controller",
     "GRAND THEFT AUTO VI LAUNCHES WORLDWIDE",
     "Midnight rollout from New Zealand; PS5, Xbox, $79.99."),
    ("building",
     "HERZOG TAPS EISENKOT TO FORM ISRAEL'S NEXT GOVERNMENT",
     "President bypasses Netanyahu to form a new government."),
]

# (section, [headlines]) in column order; columns split 15 / 15 / 15
COLUMNS = [
    [("MIDDLE EAST", [
        "Four nations urge Israel to let aid into flooded Gaza",
        "Houthis seize Red Sea coast as forces pull back to Aden",
        "Saudi-led coalition strikes Yemen, destroys missile site",
        "Egypt and Syria restore direct flights after 14 years",
        "Saudi Arabia says danger passed in three southern cities",
        "Cocaine and millions of pills seized in eastern Libya",
    ]),
     ("EUROPE", [
        "Estonia to shut Russia border crossings from 1 Dec",
        "Hundreds of thousands protest media law in Prague",
        "General strike in Spain disrupts ports and factories",
        "France faces fourth weekend of cost-of-living protests",
        "Russia and Ukraine trade drone attacks amid peace talks",
        "EU proposes \u20ac45bn Ukraine loan, repaid after reparations",
        "German police warn of rising hybrid cyber threats",
        "Russia and Vatican block gender language at COP31",
        "French minister: M\u00e9lenchon could win the presidency",
     ])],
    [("EUROPE", [
        "COP31 final talks: $120bn-a-year adaptation finance",
    ]),
     ("ASIA-PACIFIC", [
        "India evacuates ahead of Cyclone Akvan, third in a month",
        "Bangladesh garment workers in third week of protests",
        "South Korea's Lee urges APEC backing for trade and AI",
        "China and South Korea agree market access in FTA upgrade",
        "Singapore issues S$100m tokenised bills in digital currency",
        "Nvidia halts H-series and H200 chip shipments to China",
        "Explosion at Indonesia oil refinery kills one worker",
        "Cambodia urges ASEAN action over Thai occupation",
        "Most New Zealanders want MMP voting system changed",
     ]),
     ("AFRICA", [
        "Ethiopia and Eritrea mass forces along border",
        "Sudan urges arrest of ICC indictees al-Bashir, Haroun",
        "Burkina Faso targets critics in exile",
        "Five women and a boy shot dead in Botshabelo",
        "Morocco targets 50,000 defence jobs by 2035",
     ])],
    [("AMERICAS", [
        "Fed minutes: most officials expect more rate hikes",
        "Liu Yunping elected House Democratic Caucus chair",
        "US senators warn AI cyber threats outpacing defences",
        "US details $12bn Venezuela oil revenue after Maduro capture",
        "Honduras: 12 killed as Yoro declared high-risk",
        "Miami court convicts pastor over Haiti president killing",
        "Florida set for record 20th execution; Texas also executes",
        "Canada's Carney adjusts China ties, eyes right US deal",
        "Microsoft reportedly in talks to sell AI to ByteDance",
     ]),
     ("WORLD", [
        "Voyager 1 first human-made object one light-day from Earth",
        "UN: one in four women unable to refuse sex in marriage",
        "Fiji declares state of disaster amid El Ni\u00f1o drought",
        "Actor Stacy Keach dies at 85",
        "GTA VI launch to supercharge Sony; 3 in 4 units on PlayStation",
        "India vs New Zealand Test begins; Sindhu back in world top five",
     ])],
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    mx = 28  # side margin

    # Masthead
    f_mast = font(SERIF_B, 52)
    d.text((W / 2, 6), "THE WORLD", font=f_mast, fill=INK, anchor="ma")
    d.line([(mx, 64), (W - mx, 64)], fill=INK, width=2)
    d.line([(mx, 68), (W - mx, 68)], fill=INK, width=1)

    # Dateline row
    f_date = font(SANS_B, 18)
    d.text((mx, 74), "THURSDAY 19 NOVEMBER 2026", font=f_date, fill=INK)
    right = "50 STORIES \u00b7 SIX CONTINENTS"
    d.text((W - mx, 74), right, font=f_date, fill=RED, anchor="ra")

    # Dot-matrix world map strip (600x80: near-square cells, reads as a map)
    draw_map(d, 212, 98, 600, 80)

    # Lead 1
    f_lead = font(SERIF_B, 32)
    lines = wrap(LEAD1_HEAD, f_lead, W - 2 * mx)
    y = 194
    for ln in lines:
        d.text((mx, y), ln, font=f_lead, fill=INK)
        y += 37
    f_deck = font(SANS, 15)
    d.text((mx, y + 4), LEAD1_DECK, font=f_deck, fill=INK)
    y += 4 + 20
    d.line([(mx, y + 8), (W - mx, y + 8)], fill=RULE, width=1)

    # 2x2 grid of leads with icons
    f_grid_h = font(SERIF_B, 18)
    f_grid_d = font(SANS, 14)
    gy = 308
    cell_w = (W - 2 * mx - 16) // 2
    for i, (icon, head, deck) in enumerate(GRID):
        row, col = divmod(i, 2)
        cx = mx + col * (cell_w + 16)
        cy = gy + row * 62
        ICONS[icon](d, cx, cy + 6)
        tx = cx + 58
        tw = cell_w - 58
        hl = wrap(head, f_grid_h, tw)
        yy = cy
        for ln in hl:
            d.text((tx, yy), ln, font=f_grid_h, fill=INK)
            yy += 20
        d.text((tx, yy + 2), deck, font=f_grid_d, fill=INK)
    d.line([(mx, 440), (W - mx, 440)], fill=RULE, width=1)

    # Three columns of compact headlines
    f_sec = font(SANS_B, 13)
    f_item = font(SERIF_B, 13)
    col_w = (W - 2 * mx - 2 * 16) // 3
    col_ends = []
    for ci, sections in enumerate(COLUMNS):
        x = mx + ci * (col_w + 16)
        y = 448
        for sec, items in sections:
            d.rectangle([x, y, x + col_w, y + 20], fill=NAVY)
            d.text((x + 6, y + 3), sec, font=f_sec, fill=(255, 255, 255))
            y += 26
            for it in items:
                lines = wrap(it, f_item, col_w)
                for ln in lines:
                    d.text((x, y), ln, font=f_item, fill=INK)
                    y += 15
                y += 2
        col_ends.append(y)

    # Footer
    f_foot = font(SANS, 11)
    d.text((W / 2, 1000), "Compiled from reports first published on Thursday 19 November 2026",
           font=f_foot, fill=GREY, anchor="ma")

    img.save("entry.png", "JPEG", quality=95)
    print("column end y:", col_ends, " (limit 994)")
    print("saved entry.png")


if __name__ == "__main__":
    main()
