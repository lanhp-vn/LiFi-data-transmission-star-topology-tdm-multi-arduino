#include <SoftwareSerial.h>

SoftwareSerial Serial_transmit(13, A0); // RX, TX only use A0
SoftwareSerial Serial_receive(A1, 12, true); // RX, TX only use A1

const unsigned long baudrate = 700;
String data = "";

void setup() {
    Serial.begin(baudrate);
    Serial_transmit.begin(baudrate);
    Serial_receive.begin(baudrate);
}

void loop() {
    // send packet
    if (Serial_receive.available())
    {
        char c = Serial_receive.read(); // Read bytes sent from arduino 1
        Serial.print(c);
        if (c != '\0')// skip null characters
        {
            data += c; // append to the data string
            if (data.endsWith("++END++")) {
                data = data.substring(0, data.length() - 7); // remove '++END++'
                Serial_transmit.println(data); // Send the read bytes to arduino 3
                data = ""; // clear the data string
            }
        }
    }
}
