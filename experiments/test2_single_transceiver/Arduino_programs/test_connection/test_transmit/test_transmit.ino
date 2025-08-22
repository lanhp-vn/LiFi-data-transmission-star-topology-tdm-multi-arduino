// #include <Arduino.h>
#include <SoftwareSerial.h>

SoftwareSerial Serial2(4, A0); // RX, TX

const char syncword[] = "ricc";
const int syncword_length = sizeof(syncword) - 1;

// common baudrates
const unsigned long baudrates[] = {300, 1200, 9600, 19200, 38400, 57600, 115200};
int baudrate_index = 0;
int baudrate_change_timer = 0;

const char packet[] = "Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you";
const int packet_length = sizeof(packet) - 1;

// payload container
char payload[packet_length + syncword_length + 1]; // +1 for null terminator

void setup() {
    Serial.begin(115200);
    Serial.println("Transmitter ready");
}

void loop() {
    // pick a random baudrate every 7th send
    // if (baudrate_change_timer == 7) {
    //     baudrate_index = random(0, 6);
    //     baudrate_change_timer = 0;
    // } else {
    //     baudrate_change_timer++;
    // }
    baudrate_index = 1;
    Serial.print("Baudrate: ");
    Serial.println(baudrates[baudrate_index]);

    // combine packet
    strcpy(payload, syncword);
    strcat(payload, packet);

    // send packet
    Serial2.begin(baudrates[baudrate_index]);
    Serial2.write(payload);
    Serial2.end();

    // wait for 1 sec
    delay(1000);
}

