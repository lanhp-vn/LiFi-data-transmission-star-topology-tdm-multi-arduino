#include <SoftwareSerial.h>

#define TX A0
#define RX A1

SoftwareSerial Serial_transmit(13, TX);
SoftwareSerial Serial_receive(RX, 12, true);

const unsigned long baud_rate = 1200;
char data;
bool first_loop;
String timestamp = "0.00";
String buffer = "";

void setup() 
{
    Serial.begin(baud_rate);
    digitalWrite(TX, 0);
    first_loop = true;
    // Serial_transmit.begin(baud_rate);
}

void loop() 
{
    if (first_loop == true)
    {
        Serial_receive.begin(baud_rate);

        if (Serial_receive.available());
        {
            data = Serial_receive.read();
            // Serial.print(data);

            if (data != '\0') // skip null characters
            {
                buffer += data;
            }

            if (buffer.endsWith(timestamp))
            {
                Serial.print(buffer);
                buffer = "";
            } 
        }
    }

    if (Serial.available())
    {
        Serial_receive.end();
        first_loop = false;

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