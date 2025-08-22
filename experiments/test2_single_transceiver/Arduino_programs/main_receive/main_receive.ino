// #include <Arduino.h>
#include <SoftwareSerial.h>

SoftwareSerial Serial_receive(A1, 13, true); // RX, TX

const unsigned long baudrate = 700;

// data sent
char buffer;
String buffer_string;

void setup() {
    Serial.begin(baudrate);
    Serial_receive.begin(baudrate);
}

void loop() {
    // receive packet
    if (Serial_receive.available()){   
        buffer = Serial_receive.read(); // Read bytes sent from transmitter
        Serial.print(buffer); // Send the received bytes
    }
}