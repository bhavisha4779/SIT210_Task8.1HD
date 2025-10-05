#include <Wire.h>
#include <BH1750.h>
#include <ArduinoBLE.h>

BH1750 sensor;
BLEService lightService("180C");
BLEIntCharacteristic luxValue("2A6E", BLERead | BLENotify);

void setup() {
  Serial.begin(9600);
  Wire.begin();

  if (!sensor.begin()) {
    Serial.println("BH1750 error");
    while (1);
  }

  if (!BLE.begin()) {
    Serial.println("BLE error");
    while (1);
  }

  BLE.setLocalName("Nano33_BH1750");
  BLE.setAdvertisedService(lightService);
  lightService.addCharacteristic(luxValue);
  BLE.addService(lightService);
  luxValue.writeValue(0);
  BLE.advertise();

  Serial.println("Ready, waiting for Pi...");
}

void loop() {
  BLEDevice central = BLE.central();
  if (central) {
    Serial.println("Connected!");
    while (central.connected()) {
      int lux = sensor.readLightLevel();
      Serial.print("Lux: ");
      Serial.println(lux);
      luxValue.writeValue(lux);
      delay(1000);
    }
    Serial.println("Disconnected");
  }
}
