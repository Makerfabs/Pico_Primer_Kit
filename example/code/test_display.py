
# Our supplier changed the 1.8" display slightly after Jan 10, 2012
# so that the alignment of the TFT had to be shifted by a few pixels
# this just means the init code is slightly different. Check the
# color of the tab to see which init code to try. If the display is
# cut off or has extra 'random' pixels on the top & left, try the
# other option!
# If you are seeing red and green color inversion, use Black Tab
# If your TFT's plastic wrap has a Black Tab, use the following:
#  tft.initR(INITR_BLACKTAB);   // initialize a ST7735S chip, black tab
# If your TFT's plastic wrap has a Red Tab, use the following:
# tft.initR(INITR_REDTAB);   // initialize a ST7735R chip, red tab
# If your TFT's plastic wrap has a Green Tab, use the following:
# tft.initR(INITR_GREENTAB); // initialize a ST7735R chip, green tab


from ST7735 import TFT
from sysfont import sysfont
from machine import SPI, Pin
import time
import math


spi = SPI(1, baudrate=20000000, polarity=0, phase=0,
          sck=Pin(10), mosi=Pin(11), miso=None)
# def __init__( self, spi, aDC, aReset, aCS) :
tft = TFT(spi, 3, 2, 4)

tft.initg()
tft.rgb(True)


def testlines(color):
    tft.fill(TFT.BLACK)
    for x in range(0, tft.size()[0], 6):
        tft.line((0, 0), (x, tft.size()[1] - 1), color)
    for y in range(0, tft.size()[1], 6):
        tft.line((0, 0), (tft.size()[0] - 1, y), color)

    tft.fill(TFT.BLACK)
    for x in range(0, tft.size()[0], 6):
        tft.line((tft.size()[0] - 1, 0), (x, tft.size()[1] - 1), color)
    for y in range(0, tft.size()[1], 6):
        tft.line((tft.size()[0] - 1, 0), (0, y), color)

    tft.fill(TFT.BLACK)
    for x in range(0, tft.size()[0], 6):
        tft.line((0, tft.size()[1] - 1), (x, 0), color)
    for y in range(0, tft.size()[1], 6):
        tft.line((0, tft.size()[1] - 1), (tft.size()[0] - 1, y), color)

    tft.fill(TFT.BLACK)
    for x in range(0, tft.size()[0], 6):
        tft.line((tft.size()[0] - 1, tft.size()[1] - 1), (x, 0), color)
    for y in range(0, tft.size()[1], 6):
        tft.line((tft.size()[0] - 1, tft.size()[1] - 1), (0, y), color)


def testfastlines(color1, color2):
    tft.fill(TFT.BLACK)
    for y in range(0, tft.size()[1], 5):
        tft.hline((0, y), tft.size()[0], color1)
    for x in range(0, tft.size()[0], 5):
        tft.vline((x, 0), tft.size()[1], color2)


# def testgamerects(color):
 #   tft.fill(TFT.WHITE) ## How is this screen not GameEngine

  #  for i in range(game.height):
   #     for j in range(game.width):
        # OK need shapes in gameEngine
       #    TFT.rect(screen, GRAY, [
        #                    game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
        #   if game.field[i][j] > 0:
        #    TFT.rect(screen, colors[game.field[i][j]],
        #                    [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])


def testdrawrects(color):
    tft.fill(TFT.BLACK)
    for x in range(0, tft.size()[0], 6):
        tft.rect((tft.size()[0]//2 - x//2, tft.size()
                  [1]//2 - x/2), (x, x), color)


def testfillrects(color1, color2):
    tft.fill(TFT.BLACK)
    for x in range(tft.size()[0], 0, -6):
        tft.fillrect((tft.size()[0]//2 - x//2,
                      tft.size()[1]//2 - x/2), (x, x), color1)
        tft.rect((tft.size()[0]//2 - x//2, tft.size()
                  [1]//2 - x/2), (x, x), color2)


def testfillcircles(radius, color):
    for x in range(radius, tft.size()[0], radius * 2):
        for y in range(radius, tft.size()[1], radius * 2):
            tft.fillcircle((x, y), radius, color)


def testdrawcircles(radius, color):
    for x in range(0, tft.size()[0] + radius, radius * 2):
        for y in range(0, tft.size()[1] + radius, radius * 2):
            tft.circle((x, y), radius, color)


def testtriangles():
    tft.fill(TFT.BLACK)
    color = 0xF800
    w = tft.size()[0] // 2
    x = tft.size()[1] - 1
    y = 0
    z = tft.size()[0]
    for t in range(0, 15):
        tft.line((w, y), (y, x), color)
        tft.line((y, x), (z, x), color)
        tft.line((z, x), (w, y), color)
        x -= 4
        y += 4
        z -= 4
        color += 100


def testroundrects():
    tft.fill(TFT.BLACK)
    color = 100
    for t in range(5):
        x = 0
        y = 0
        w = tft.size()[0] - 2
        h = tft.size()[1] - 2
        for i in range(17):
            tft.rect((x, y), (w, h), color)
            x += 2
            y += 3
            w -= 4
            h -= 6
            color += 1100
        color += 100


def tftprinttest():
    tft.fill(TFT.BLACK)
    v = 30
    tft.text((0, v), "Hello World!", TFT.RED, sysfont, 1, nowrap=True)
    v += sysfont["Height"]
    tft.text((0, v), "Hello World!", TFT.YELLOW, sysfont, 2, nowrap=True)
    v += sysfont["Height"] * 2
    tft.text((0, v), "Hello World!", TFT.GREEN, sysfont, 3, nowrap=True)
    v += sysfont["Height"] * 3
    tft.text((0, v), str(1234.567), TFT.BLUE, sysfont, 4, nowrap=True)
    time.sleep_ms(1500)
    tft.fill(TFT.BLACK)
    v = 0
    tft.text((0, v), "Hello World!", TFT.RED, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), str(math.pi), TFT.GREEN, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), " Want pi?", TFT.GREEN, sysfont)
    v += sysfont["Height"] * 2
    tft.text((0, v), hex(8675309), TFT.GREEN, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), " Print HEX!", TFT.GREEN, sysfont)
    v += sysfont["Height"] * 2
    tft.text((0, v), "Sketch has been", TFT.WHITE, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), "running for: ", TFT.WHITE, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), str(time.ticks_ms() / 1000), TFT.PURPLE, sysfont)
    v += sysfont["Height"]
    tft.text((0, v), " seconds.", TFT.WHITE, sysfont)
    tft.fill(TFT.BLACK)
    tft.text((0, 0), "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur adipiscing ante sed nibh tincidunt feugiat. Maecenas enim massa, fringilla sed malesuada et, malesuada sit amet turpis. Sed porttitor neque ut ante pretium vitae malesuada nunc bibendum. Nullam aliquet ultrices massa eu hendrerit. Ut sed nisi lorem. In vestibulum purus a tortor imperdiet posuere. ", TFT.WHITE, sysfont, 1)
    time.sleep_ms(1000)

    # def rect( self, aStart, aSize, aColor ) :
    '''Draw a hollow rectangle.  aStart is the smallest coordinate corner
       and aSize is a tuple indicating width, height.'''


def testdrawarects(color):
    tft.fill(TFT.BLACK)

    tft.rect((tft.size()[0]//2, tft.size()
              [1]//2), (50, 100), color)

    tft.rect((1, 1), (127, 159), TFT.RED)
    print(str(tft.size()[0]//2))


def testgrid():
    x = 4
    y = 10
    tft.fill(TFT.BLACK)
    for i in range(0, 10):
        for j in range(0, 20):
            tft.rect((x + 12 * i, y + 7*j - 1), (120//10, 155//20), TFT.RED)
          #  if (j % 2) == 1  and (i % 2) == 1 :
    time.sleep_ms(4000)
    for i in range(0, 10):
        for j in range(0, 20):
            tft.fillrect((x + 12 * i + 1, y + 7 * j),
                         (120//10-2, 155//20-2), TFT.BLUE)
    time.sleep_ms(4000)


def testblockColor():
    vPos = 80
    fSize = 2
    aColor = TFT.RED
    tft.fill(TFT.BLACK)
    tft.text((8, vPos), "TFT.BLACK", aColor, sysfont, fSize, nowrap=True)
    time.sleep_ms(1000)
    aColor = TFT.BLACK
    tft.fill(TFT.RED)
    tft.text((8, vPos), "TFT.RED", aColor, sysfont, fSize, nowrap=True)
    time.sleep_ms(1000)
    tft.fill(TFT.MAROON)
    tft.text((8, vPos), "TFT.MAROON", aColor, sysfont, fSize, nowrap=True)
    time.sleep_ms(1000)

    tft.fill(TFT.GOLD)
    tft.text((8, vPos), "TFT.GOLD", aColor, sysfont, fSize, nowrap=True)
    time.sleep_ms(1000)
    tft.fill(TFT.GREEN)
    tft.text((8, vPos), "TFT.GREEN", aColor, sysfont, fSize, nowrap=True)
    time.sleep_ms(1000)
    tft.fill(TFT.FOREST)
    tft.text((8, vPos), "TFT.FOREST", aColor, sysfont, fSize, nowrap=True)
    time.sleep_ms(1000)
    tft.fill(TFT.BLUE)
    tft.text((8, vPos), "TFT.BLUE", aColor, sysfont, fSize, nowrap=True)
    time.sleep_ms(1000)
    tft.fill(TFT.NAVY)
    tft.text((8, vPos), "TFT.NAV", aColor, sysfont, fSize, nowrap=True)
    time.sleep_ms(1000)
    tft.fill(TFT.CYAN)
    tft.text((8, vPos), "TFT.CYAN", aColor, sysfont, fSize, nowrap=True)
    time.sleep_ms(1000)
    tft.fill(TFT.YELLOW)
    tft.text((8, vPos), "TFT.YELLOW", aColor, sysfont, fSize, nowrap=True)
    time.sleep_ms(1000)
    tft.fill(TFT.PURPLE)
    tft.text((8, vPos), "TFT.PURPLE", aColor, sysfont, fSize, nowrap=True)
    time.sleep_ms(1000)
    tft.fill(TFT.WHITE)
    tft.text((8, vPos), "TFT.WHITE", aColor, sysfont, fSize, nowrap=True)
    time.sleep_ms(1000)
    tft.fill(TFT.GRAY)
    tft.text((8, vPos), "TFT.GRAY", aColor, sysfont, fSize, nowrap=True)
    time.sleep_ms(1000)

    tft.fill(TFT.ORANGE)
    tft.text((8, vPos), "TFT.ORANGE", aColor, sysfont, fSize, nowrap=True)
    time.sleep_ms(1000)


def test_main():

    time.sleep_ms(1000)

    testgrid()
    testblockColor()

    # def test_main_org():
    print("Start main")
    tft.fill(TFT.BLACK)

    tftprinttest()
    time.sleep_ms(4000)
    print("test  Y line")
    testlines(TFT.YELLOW)
    time.sleep_ms(500)
    print("fast  line")
    testfastlines(TFT.RED, TFT.BLUE)
    time.sleep_ms(500)

    testdrawrects(TFT.GREEN)
    time.sleep_ms(500)

    testfillrects(TFT.YELLOW, TFT.PURPLE)
    time.sleep_ms(500)

    tft.fill(TFT.BLACK)
    testfillcircles(10, TFT.BLUE)
    testdrawcircles(10, TFT.WHITE)
    time.sleep_ms(500)

    testroundrects()
    time.sleep_ms(500)

    testtriangles()
    time.sleep_ms(500)

    testdrawarects(TFT.GREEN)
    time.sleep_ms(500)
    testgrid()


def test_debug():
    tft.fill(TFT.BLACK)
#    tft.rect((0, 0), (10, 10), TFT.WHITE)
#     tft.rect((100, 100), (10, 10), TFT.WHITE)
#    tft.text((0, 0), "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur adipiscing ante sed nibh tincidunt feugiat. Maecenas enim massa, fringilla sed malesuada et, malesuada sit amet turpis. Sed porttitor neque ut ante pretium vitae malesuada nunc bibendum. Nullam aliquet ultrices massa eu hendrerit. Ut sed nisi lorem. In vestibulum purus a tortor imperdiet posuere. ", TFT.WHITE, sysfont, 1)
    while True:
        tft.fill(TFT.BLUE)
        tft.text((8, 40), "TFT.BLUE", TFT.WHITE, sysfont, 2)
        time.sleep_ms(1000)

        tft.fill(TFT.RED)
        tft.text((8, 40), "TFT.RED", TFT.WHITE, sysfont, 2)
        time.sleep_ms(1000)

        tft.fill(TFT.GREEN)
        tft.text((8, 40), "TFT.GREEN", TFT.WHITE, sysfont, 2)
        time.sleep_ms(1000)
    pass


if __name__ == "__main__":
    test_main()
    # test_debug()
