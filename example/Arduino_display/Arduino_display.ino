#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library for ST7735
#include <SPI.h>

#include "a1.h"
#include "pic1.h"
#include "pic2.h"

#define TFT_CS 13
#define TFT_RST 15 // Or set to -1 and connect to Arduino RESET pin
#define TFT_DC 14

#define SPI_MOSI 11
#define SPI_MISO 12
#define SPI_SCK 10

Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_RST);

void setup(void)
{
    Serial.begin(115200);
    Serial.print(F("Hello! ST77xx TFT Test"));

    SPI = MbedSPI(SPI_MISO, SPI_MOSI, SPI_SCK);

    // OR use this initializer (uncomment) if using a 1.44" TFT:
    tft.initR(INITR_144GREENTAB); // Init ST7735R chip, green tab

    Serial.println(F("Initialized"));

    tft.fillScreen(ST77XX_BLACK);
}

void loop()
{
    //Show logo
    tft.drawRGBBitmap(0, 0, a1, 128, 128);
    delay(3000);
    tft.drawRGBBitmap(0, 0, pic1, 128, 128);
    delay(3000);
    tft.drawRGBBitmap(0, 0, pic2, 128, 128);
    delay(3000);
}
