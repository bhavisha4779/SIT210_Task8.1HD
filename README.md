# SIT210 – Task 8.1HD – Bluetooth Parking System  

## 📌 Project Idea  
This project shows how to use **Arduino Nano 33 IoT** as a **sensor** and **Raspberry Pi** as an **actuator**.  
- The Arduino reads **light values** from a **BH1750 sensor**.  
- It sends the values to the Raspberry Pi using **Bluetooth**.  
- The Raspberry Pi uses the value to control an **LED**.  
- The LED behavior changes based on the light level.  

This is similar to a **reverse parking sensor** in a car.  

---

## 🔧 Hardware Used  
- Arduino Nano 33 IoT  
- BH1750 Light Ambient Sensor  
- Raspberry Pi (with Bluetooth)  
- LED (any color)  
- 220Ω Resistor  
- Breadboard and jumper wires  

---

## 🔌 Wiring Connections  

### Arduino + BH1750  
| BH1750 Pin | Arduino Pin  |  
|------------|--------------|  
| VCC        | 3.3V         |  
| GND        | GND          |  
| SCL        | A5 (SCL)     |  
| SDA        | A4 (SDA)     |  
| ADD        | GND          |  

### Raspberry Pi + LED  
| Component  | Pi Physical Pin |  
|------------|-----------------|  
| LED Anode (+) | Pin 12 (GPIO18, PWM) |  
| LED Cathode (–) | Resistor → Pin 6 (GND) |  

---

## 💻 Software Setup  

### Arduino  
1. Open Arduino IDE.  
2. Install libraries:  
   - **BH1750**  
   - **ArduinoBLE**  
3. Upload `arduino_sensor.ino` to Arduino Nano 33 IoT.  

---

### Raspberry Pi  
1. Install Python 3 and pip.  
2. Install packages:  
   ```bash
   pip3 install bleak RPi.GPIO --break-system-packages

   ---
   
### Run_Script:
1. command: "python3 led_control.py"

---

### LED_Behavior_Thresholds:
  1. condition: "Dark (lux < 50)"
    action: "LED is OFF"
  2. condition: "Medium light (50–200)"
    action: "LED blinks slowly (1 second on/off)"
  3. condition: "Bright light (≥200)"
    action: "LED blinks fast (0.1s on/off)"

---

### Conclusion:
  - "Arduino works as a sensor device."
  - "Raspberry Pi works as an actuator."
  - "They communicate using Bluetooth."
  - "Sensor data changes LED action."
