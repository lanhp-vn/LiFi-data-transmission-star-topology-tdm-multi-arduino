#include <SoftwareSerial.h>

#define TX A0
#define RX A1

SoftwareSerial Serial_transmit(13, TX);
SoftwareSerial Serial_receive(RX, 12, true);

const unsigned long baud_rate = 1200;
String endSignal_router = "---";
String timestamp = "0.00";
float interval = 3.9000000000000004;
long millis_interval = interval * 1000;
long previousMillis = -millis_interval;  // will store last time the serial data was updated;
long currentMillis;
long elapsedMillis;

String buffer = "";
String packet = "";

char data;
bool first_loop;

void setup() 
{
    Serial.begin(baud_rate);
    // Serial_receive.begin(baud_rate);
    first_loop = true;
}

void loop() 
{
    currentMillis = millis();
    elapsedMillis = currentMillis - previousMillis;

    if (Serial_receive.available())
    {
        first_loop = false;
        // Serial.println("receiving");
        data = Serial_receive.read();
        // Serial.print(data);
        if (data != '\xff') // skip null characters
        {
            buffer += data;
        }
    }
    
    // Check if the interval has passed; if so, transmit to PC
    if (elapsedMillis >= millis_interval)
    {  
        Serial_receive.end();
        Serial_transmit.begin(baud_rate);

        if (buffer.length() > 0)
        {
            packet += buffer;
            packet += endSignal_router;
            Serial_transmit.print(packet);
        }
        
        if (first_loop == true)
        {
            Serial_transmit.begin(baud_rate);
            // Serial.print(first_loop);
            Serial_transmit.print(timestamp);
            Serial_transmit.end();
        }
        
        // Clear the packet string and buffer string for the next use
        packet = "";
        buffer = "";

        Serial_transmit.end();  
        Serial_receive.begin(baud_rate);

        // save the last time the serial data was updated
        previousMillis = currentMillis;
    }
}
