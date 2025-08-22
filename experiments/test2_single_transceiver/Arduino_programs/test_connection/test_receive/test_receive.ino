// #include <Arduino.h>
#include <SoftwareSerial.h>

SoftwareSerial Serial2(A1, 4, true); // RX, TX

const char syncword[] = "ricc";
const int syncword_length = sizeof(syncword) - 1;

// common baudrates
const unsigned long baudrates[] = {300, 1200, 9600, 19200, 38400, 57600, 115200};
int baudrate_index = 0;

const char packet[] = "Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you";
const int packet_length = sizeof(packet) - 1;
int error_count = 1;

// payload container
char payload[packet_length + syncword_length + 1]; // +1 for null terminator
String payload_string;

void setup() {
    Serial.begin(115200);
    Serial.println("Receiver ready");

    baudrate_index = 1;

    // assume first index baudrate
    Serial2.begin(baudrates[baudrate_index]);
}

void loop() {
    // receive packet
    if (Serial2.available()) {
        Serial.println("Packet received: ");
        // store packet
        Serial2.readBytes(payload, packet_length + syncword_length);
        // print packet
        Serial.println(payload);

        // copy payload to string
        payload_string = payload;

        // check for syncword in packet
        if (payload_string.indexOf(syncword) != -1) {
            // remove syncword from packet
            payload_string.remove(0, syncword_length);
            // print packet
            Serial.println("Packet: ");
            Serial.println(payload_string);
        }

        // compare packet to original
        for (int i = 0; i < packet_length; i++) {
            if (payload_string[i] != packet[i]) {
                error_count++;
            }
        }

        // print error count
        Serial.print("Error count: ");
        Serial.println(error_count);

        // calculate error rate
        float error_rate = (float)error_count / (float)packet_length;
        Serial.print("Error rate: ");
        Serial.println(error_rate);

        error_count = 0; // reset error count
        Serial.println();
    }

    // Serial.print(digitalRead(3));
    // delay(1);
    // when not found, jump to next baudrate
    // else {
    //     // print baudrate
    //     Serial.print("Baudrate: ");
    //     Serial.println(baudrates[baudrate_index]);
    //     // print packet
    //     Serial.println("Packet: ");
    //     Serial.println(payload + syncword_length);
    //     // jump to next baudrate
    //     baudrate_index++;
    //     if (baudrate_index > 5) {
    //         baudrate_index = 0;
    //     }
    //     Serial2.end();
    //     Serial2.begin(baudrates[baudrate_index]);
    // }

}