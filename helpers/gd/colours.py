def rgb_to_hex(col: str):
    if not col:
        col = "255, 255, 255"

    r = col.split(",")[0]
    b = col.split(",")[1]
    g = col.split(",")[2]

    if '#' in b:
        b = b.split("#")[0]

    r_hex = format(int(r), '02x')
    g_hex = format(int(g), '02x')
    b_hex = format(int(b), '02x')

    return ("0" + r_hex if len(r_hex) == 1 else r_hex,
            "0" + g_hex if len(g_hex) == 1 else g_hex,
            "0" + b_hex if len(b_hex) == 1 else b_hex)

