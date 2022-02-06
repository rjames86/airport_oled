from draw import OLEDDraw

if __name__ == '__main__':
    d = OLEDDraw()
    try:
        while True:
            d.write_screen()
    except KeyboardInterrupt:
        d.clear_screen()
        
