#include "CmdMessenger.h"
#include "SPI.h"
#include "U8g2lib.h"

//U8G2_PCD8544_84X48_1_4W_SW_SPI u2g8nokia(
//    U8G2_R0, 
//  /* clk=*/ 7, 
//  /* din=*/ 6, 
//  /* ce=*/ 5, 
//  /* dc=*/ 4, 
//  /* rst=*/ 3
//);
//
//U8G2_SSD1306_128X64_NONAME_1_4W_SW_SPI u8g2oled(
//  U8G2_R0, 
//  /* d0=*/ 13, 
//  /* d1=*/ 11, 
//  /* cs=*/ 10, 
//  /* dc=*/ 9, 
//  /* rst=*/ 8
//);

U8G2_PCD8544_84X48_1_4W_SW_SPI u2g8nokia(
    U8G2_R0, 
  /* clock=*/ 7, 
  /* data=*/ 6, 
  /* ce=*/ 5, 
  /* dc=*/ 4, 
  /* reset=*/ 3
);

U8G2_SSD1306_128X64_NONAME_1_4W_SW_SPI u8g2oled(
  U8G2_R0, 
  /* clock=*/ 7, 
  /* data=*/ 6, 
  /* cs=*/ 10, 
  /* dc=*/ 9, 
  /* reset=*/ 8
);

/* Define available CmdMessenger commands */
enum {
    data_nokia,
    data_oled,
    data_ksp,
    error,
};

/* Initialize CmdMessenger -- this should match PyCmdMessenger instance */
const int BAUD_RATE = 9600;
CmdMessenger c = CmdMessenger(Serial,',',';','/');

/* Draw function for Nokia */
void draw_nokia(long int alt, long int ap, long int pe, float twr, long int dv, int g) {
  String tmpStr;
  u2g8nokia.firstPage();
  do {
    char string[10];
    
    //dtostrf(alt, 10, 0, string);
    u2g8nokia.drawStr(0, 8,  "ALT: ");
    u2g8nokia.setCursor(25, 8);
    u2g8nokia.print(alt);
    
    //dtostrf(ap, 10, 0, string);
    u2g8nokia.drawStr(0, 16,  "AP : ");
    u2g8nokia.setCursor(25, 16);
    u2g8nokia.print(ap);
    
    //dtostrf(pe, 10, 0, string);
    u2g8nokia.drawStr(0, 24,  "PE : ");
    if (pe < 0) u2g8nokia.setCursor(20, 24);
    else if (pe > 0) u2g8nokia.setCursor(25, 24);
    u2g8nokia.print(pe);

    //dtostrf(twr, 10, 2, string);
    u2g8nokia.drawStr(0, 32,  "TWR: ");
    u2g8nokia.setCursor(25, 32);
    u2g8nokia.print(twr);
    
    //dtostrf(dv, 10, 0, string);
    u2g8nokia.drawStr(0, 40,  "DV : ");
    u2g8nokia.setCursor(25, 40);
    u2g8nokia.print(dv);
    
    //dtostrf(g, 10, 0, string);
    u2g8nokia.drawStr(0, 48,  "G  : ");
    u2g8nokia.setCursor(25, 48);
    u2g8nokia.print(g);
    
  } while (u2g8nokia.nextPage());
}

void drawResources(float monoprop, float liquid, float oxidiser, float charge) {
  
}

void draw_oled(float lf, float ox, float mp, float ec) {
  u8g2oled.firstPage();
  do {
    int lengthBox;
    const int boxMaxLength = 90;
    
    lengthBox = (int)round(lf*boxMaxLength);
    u8g2oled.drawStr(0, 16, "LF");
    u8g2oled.drawFrame(38, 4, 90, 12);
    u8g2oled.drawBox(38, 4, lengthBox, 12);
  
    lengthBox = (int)round(ox*boxMaxLength);
    u8g2oled.drawStr(0, 32, "OX");
    u8g2oled.drawFrame(38, 20, 90, 12);
    u8g2oled.drawBox(38, 20, lengthBox, 12);
    
    lengthBox = (int)round(mp*boxMaxLength);
    u8g2oled.drawStr(0, 48, "MP");
    u8g2oled.drawFrame(38, 36, 90, 12);
    u8g2oled.drawBox(38, 36, lengthBox, 12);
    
    lengthBox = (int)round(ec*boxMaxLength);
    u8g2oled.drawStr(0, 64, "EC");
    u8g2oled.drawFrame(38, 52, 90, 12);
    u8g2oled.drawBox(38, 52, lengthBox, 12);
  } while(u8g2oled.nextPage());
}

/* Create callback functions to deal with incoming messages */

/* callback */
void on_data_nokia(void){
    //Display stuff here
    long int alt = c.readBinArg<long>();
    long int ap = c.readBinArg<long>();
    long int pe = c.readBinArg<long>();
    float twr = c.readBinArg<float>();
    long int dv = c.readBinArg<long>();
    int g = c.readBinArg<int>();

    draw_nokia(alt, ap, pe, twr, dv, g);
}

/* callback */
void on_data_oled(void) {
  float p_lf = c.readBinArg<int>() / 100.0;
  float p_ox = c.readBinArg<int>() / 100.0;
  float p_mp = c.readBinArg<int>() / 100.0;
  float p_ec = c.readBinArg<int>() / 100.0;

  draw_oled(p_mp, p_lf, p_ox, p_ec);
}

/* callback */
void on_unknown_command(void){
    c.sendCmd(error,"Command without callback.");
}

/* Attach callbacks for CmdMessenger commands */
void attach_callbacks(void) { 
  
    c.attach(data_nokia, on_data_nokia);
    c.attach(data_oled, on_data_oled);
    c.attach(on_unknown_command);
}

void setup() {
    Serial.begin(BAUD_RATE);
    u2g8nokia.begin();
    u2g8nokia.setFont(u8g2_font_5x7_mf);
    u8g2oled.begin();
    u8g2oled.setFont(u8g2_font_crox3cb_mr);
    attach_callbacks();    
}

void loop() {
    c.feedinSerialData();
}
