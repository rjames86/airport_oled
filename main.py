from draw import OLEDDraw

if __name__ == "__main__":
    d = OLEDDraw()
    try:
        while True:
            d.write_screen()
    except Exception:
        d.clear_screen()
