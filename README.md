# RFID-Based Attendance Logger – Personal Project
This project logs student attendance using **RFID card scanning** and **real-time serial communication**, built with **Arduino UNO**, **RFID Reader (MFRC522)**, and a Python-based backend system. 
It was developed as part of a college hackathon under **Keshav Memorial College of Engineering**, where it won **1st place**.


## 🏆 Achievements

- **Winner of Hackathon 2025** – Recognized for practical implementation, innovation, and system design  
- Project idea proposed and developed as a core solution for smart campus management


## 🔗 Team Repository

👉 Full team repo: [github.com/jithender2005/TV-T-30-RFID-Reader-/tree/main/project](https://github.com/jithender2005/TV-T-30-RFID-Reader-/tree/main/project)


## My Contributions
- Proposed and pitched the **project idea** for the hackathon  
- Set up **Arduino UNO**, **RFID scanner**, **RTC module**, and **LCD display**  
- Designed the **architecture and circuit diagram** (`hackarch.drawio`)  
- Participated in live demo, testing, and explaining technical workflow during judging


## Tech Stack
- **Hardware**: Arduino UNO, MFRC522 RFID Reader, DS3231 RTC Module, 16x2 LCD Display  
- **Software**: Python (Serial Reader, Attendance Logger), SQLite/MySQL  
- **Tools**: VS Code, draw.io



## Key Files
- `attendance_logger.py`: Python script for listening to serial input and logging attendance  
- `hackarch.drawio`: Architecture and circuit diagram  
- *(Team repo contains full Arduino code and web interface)*



## 🧪 How It Works
1. RFID tag is scanned  
2. Arduino sends UID to serial port  
3. Python script maps UID to student and logs attendance if not marked already  
4. LCD displays status (Marked/Already Marked/Unknown UID)
