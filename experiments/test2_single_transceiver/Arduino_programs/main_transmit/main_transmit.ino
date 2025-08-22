#include <SoftwareSerial.h>

SoftwareSerial Serial_transmit(13, A0); // RX, TX

const unsigned long baudrate = 700;
char data;

void setup() {
    Serial.begin(baudrate);
    // digitalWrite(A0, 0);
    // Serial_transmit.begin(baudrate);
}

void loop() {
    
    Serial_transmit.begin(baudrate);

    // send packet
    if (Serial.available())
    {
        // digitalWrite(A0,1);
        data = Serial.read(); // Read bytes sent from PC
        Serial_transmit.write(data); // Send the read bytes to the receiver
    }
    // else
    // {
    //     digitalWrite(A0,0);
    // }

    Serial_transmit.end();
}