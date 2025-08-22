#include <SoftwareSerial.h>

#define TX A0
#define RX A1

SoftwareSerial Serial_transmit(13, TX);
// SoftwareSerial Serial_receive(RX, 12, true);

const unsigned long baud_rate = 1200;
char data;

void setup() 
{
    Serial.begin(baud_rate);
    digitalWrite(TX, 0);
    // Serial_transmit.begin(baud_rate);
}

void loop() 
{
    if (Serial.available())
    {
        Serial_transmit.begin(baud_rate);
        digitalWrite(TX, 1);
        data = Serial.read();
        Serial_transmit.print(data);
    }

    else
    {
        Serial_transmit.end();
        digitalWrite(TX, 0);
    }
   
}