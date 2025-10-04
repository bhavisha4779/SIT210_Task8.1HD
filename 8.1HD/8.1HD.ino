#include <Wire.h>
#include <BH1750.h>
#include <ArduinoBLE.h>

BH1750 lightMeter;

BLEService lightService("180C");           // Custom service
BLEIntCharacteristic luxCharacteristic("2A6E", BLERead | BLENotify);

void setup() {
  Serial.begin(9600);
  while (!Serial);

  // Start I2C
  Wire.begin();
  if (lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE)) {
    Serial.println("BH1750 initialized");
  } else {
    Serial.println("Error initializing BH1750");
    while (1);
  }

  // Start BLE
  if (!BLE.begin()) {
    Serial.println("Error starting BLE!");
    while (1);
  }

  BLE.setLocalName("Nano33_BH1750");
  BLE.setAdvertisedService(lightService);

  lightService.addCharacteristic(luxCharacteristic);
  BLE.addService(lightService);

  luxCharacteristic.writeValue(0);

  BLE.advertise();
  Serial.println("BLE device active, waiting for connections...");
}

void loop() {
  // Wait for central device (Raspberry Pi)
  BLEDevice central = BLE.central();

  if (central) {
    Serial.print("Connected to: ");
    Serial.println(central.address());

    while (central.connected()) {
      float lux = lightMeter.readLightLevel();
      Serial.print("Light: ");
      Serial.print(lux);
      Serial.println(" lx");

      // Send lux value over BLE
      luxCharacteristic.writeValue((int)lux);

      delay(1000); // send every second
    }

    Serial.println("Central disconnected");
  }
}
