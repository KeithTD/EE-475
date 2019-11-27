#include <SoftwareSerial.h> //Used for transmitting to the device
SoftwareSerial softSerial(2, 3); //RX, TX

#include "SparkFun_UHF_RFID_Reader.h" //Library for controlling the M6E Nano module
RFID nano; //Create instance

#define BUZZER1 9
#define BUZZER2 10

long timer;
char entry;
char day;

int txtCount;
int notCount;
int lapCount;
int bagCount;

char archive[10][12];
int archiveCount;

void setup() {
  Serial.begin(115200);
  while (!Serial);

  pinMode(BUZZER1, OUTPUT);
  pinMode(BUZZER2, OUTPUT);
  digitalWrite(BUZZER2, LOW); //Pull half the buzzer to ground and drive the other half.

  txtCount = 0;
  notCount = 0;
  lapCount = 0;
  bagCount = 0;
  archiveCount = 0;
  
  if (setupNano(38400) == false) //Configure nano to run at 38400bps
  {
    Serial.println("Module failed to respond. Please check wiring.");
    while (1); //Freeze!
  }

  nano.setRegion(REGION_NORTHAMERICA); //Set to North America
  nano.setReadPower(500);
  nano.setWritePower(500);
}

void loop() {
  Serial.println("Ready");
  while (!Serial.available()); //Wait for user to send a character
  entry = Serial.read();

  if (entry == '1') {
    checkRFID();
  }
  else if (entry == '2') {
    addRFID();
  }
  else if (entry == '3') {
    modRFID();
  } 
  else if (entry == '4') {
    checkArchive();
  }
  else {
    Serial.println("Please use a valid command.");
  }
}

void modRFID() {
  char catchDays[7];
  int catchCount = 0;
  char writeEPC[] = {0, 0, 0, 0, 0, 'm', 't', 'w', 'r', 'f', 's', 'n'};
  
  Serial.println("m or d");
  while(!Serial.available());
  char entry = Serial.read();
  
  if (entry == 'm') {
    Serial.println("which days?");
    while (!Serial.available());
    while (Serial.available() > 0) {
      catchDays[catchCount] = Serial.read();
      catchCount++;
      delay(50);
    }
    for (int i = 0; i < catchCount; i++) {
      if (catchDays[i] == 'm' || catchDays[i] == 'M') {
        writeEPC[5] = 'M';
      } else if (catchDays[i] == 'n' || catchDays[i] == 'N') {
        writeEPC[11] = 'N';
      } else if (catchDays[i] == 't' || catchDays[i] == 'T') {
        writeEPC[6] = 'T';
      } else if (catchDays[i] == 'w' || catchDays[i] == 'W') {
        writeEPC[7] = 'W';
      } else if (catchDays[i] == 'r' || catchDays[i] == 'R') {
        writeEPC[8] = 'R';
      } else if (catchDays[i] == 'f' || catchDays[i] == 'F') {
        writeEPC[9] = 'F';
      } else if (catchDays[i] == 's' || catchDays[i] == 'S') {
        writeEPC[10] = 'S';
      }
    }

    Serial.println("hit key");
    while (!Serial.available());
    Serial.read();
    
    byte myEPC[12]; //Most EPCs are 12 bytes
    byte myEPClength;
    byte responseType = 0;
  
    while (responseType != RESPONSE_SUCCESS)//RESPONSE_IS_TAGFOUND)
    {
      myEPClength = sizeof(myEPC); //Length of EPC is modified each time .readTagEPC is called
  
      responseType = nano.readTagEPC(myEPC, myEPClength, 500); //Scan for a new tag up to 500ms
      //Serial.println(F("Searching for tag"));
    }
    for (int i = 0; i < 5; i++) {
      writeEPC[i] = myEPC[i];
    }
    writeRFID(writeEPC);

    for (int i = 0; i < archiveCount; i++) {
      for (int j = 0; j < 5; j++) {
        if (archive[i][j] != myEPC[j])
          break;
        if (j == 4) {
          for (int k = 5; k < 12; k++) {
            archive[i][k] = writeEPC[k];
          }
        }
      }
    }
  } 
  else if (entry == 'd') {
    for (int i = 0; i < 12; i++) {
      writeEPC[i] = random(256);
    }
    Serial.println("hit key");
    while (!Serial.available());
    Serial.read();
    
    byte myEPC[12]; //Most EPCs are 12 bytes
    byte myEPClength;
    byte responseType = 0;
    while (responseType != RESPONSE_SUCCESS) {
      myEPClength = sizeof(myEPC); //Length of EPC is modified each time .readTagEPC is called
      responseType = nano.readTagEPC(myEPC, myEPClength, 500); //Scan for a new tag up to 500ms
    }
    writeRFID(writeEPC);
    
    for (int i = 0; i < archiveCount; i++) {
      for (int j = 0; j < 12; j++) {
        if (archive[i][j] != myEPC[j]) {
          break;
        }
        if (j == 11) {
          for (int k = i; k < archiveCount - 1; k++) {
            for (int l = 0; l < 12; l++) {
              archive[k][l] = archive[k + 1][l];
            }
          }
          archiveCount--;
        }
      }
    }

    
  } 
  else {
    Serial.println("WRONG");
  }
}

void addRFID() {
  char catchDays[7];
  int catchCount = 0;
  char writeEPC[] = {0, 0, 0, 0, 0, 'm', 't', 'w', 'r', 'f', 's', 'n'};
  char type;
  
  Serial.println("which days?");
  while (!Serial.available());
  while (Serial.available() > 0) {
    catchDays[catchCount] = Serial.read();
    catchCount++;
    delay(50);
  }
  
  for (int i = 0; i < catchCount; i++) {
    if (catchDays[i] == 'm' || catchDays[i] == 'M') {
      writeEPC[5] = 'M';
    } else if (catchDays[i] == 'n' || catchDays[i] == 'N') {
      writeEPC[11] = 'N';
    } else if (catchDays[i] == 't' || catchDays[i] == 'T') {
      writeEPC[6] = 'T';
    } else if (catchDays[i] == 'w' || catchDays[i] == 'W') {
      writeEPC[7] = 'W';
    } else if (catchDays[i] == 'r' || catchDays[i] == 'R') {
      writeEPC[8] = 'R';
    } else if (catchDays[i] == 'f' || catchDays[i] == 'F') {
      writeEPC[9] = 'F';
    } else if (catchDays[i] == 's' || catchDays[i] == 'S') {
      writeEPC[10] = 'S';
    }
  }
  
  Serial.println("type?");
  while (!Serial.available());
  type = Serial.read();
  
  if (type == 't' || type == 'T') {
    writeEPC[0] = 'T';
    writeEPC[1] = 'X';
    writeEPC[2] = 'T';
    writeEPC[3] = txtCount;
    txtCount++;
  } else if (type == 'n' || type == 'N') {
    writeEPC[0] = 'N';
    writeEPC[1] = 'O';
    writeEPC[2] = 'T';
    writeEPC[3] = notCount;
    notCount++;
  } else if (type == 'l' || type == 'L') {
    writeEPC[0] = 'L';
    writeEPC[1] = 'A';
    writeEPC[2] = 'P';
    writeEPC[3] = lapCount;
    lapCount++;
  }  else if (type == 'b' || type == 'B') {
    writeEPC[0] = 'B';
    writeEPC[1] = 'A';
    writeEPC[2] = 'G';
    writeEPC[3] = bagCount;
    bagCount++;
  }

  Serial.println("hit key");
  while (!Serial.available());
  Serial.read();
  writeRFID(writeEPC);
  
  for (int i = 0; i < 12; i++) {
    archive[archiveCount][i] = writeEPC[i];
  }
  archiveCount++;
}

void checkRFID() {
  Serial.println("Enter day:");
  while (!Serial.available());
  day = Serial.read(); 
  Serial.println("Begin");

  int caughtCount = 0; 
  char epc[12];
  char epcCaught[10][12];
  bool match = false;
  int sectMatch = 0;

  for (int i = 0; i < 10; i++) {
    for (int j = 0; j < 12; j++) {
      epcCaught[i][j] = 0;
    }
  }
  
  nano.startReading();
  timer = millis();
  
  while (millis() - timer < 10000) {
    if (nano.check() == true) //Check to see if any new data has come in from module
    {
      byte responseType = nano.parseResponse(); //Break response into tag ID, RSSI, frequency, and timestamp
      if (responseType == RESPONSE_IS_KEEPALIVE){
      } 
      else if (responseType == RESPONSE_IS_TAGFOUND) {
        byte tagEPCBytes = nano.getTagEPCBytes(); //Get the number of bytes of EPC from response
        for (byte x = 0 ; x < tagEPCBytes ; x++) {
          epc[x] = (char)nano.msg[31 + x];
        }

        for (int i = 0; i < 10; i++) {
          for (int j = 0; j < 12; j++) {
            if (epcCaught[i][j] == epc[j]) {
              sectMatch++;
            }
            if (j == 11 && sectMatch == 12) {
              match = true;
            }
          }
          sectMatch = 0;
          if (i == 9 && !match) {
            for (int k = 0; k < 12; k++) {
              epcCaught[caughtCount][k] = epc[k];
              if (k == 3) {
                Serial.print((int)epc[k]);
              }
              else
                Serial.print(epc[k]);
            }
            caughtCount++;
            Serial.println();
          }
        }
        match = false;
      }
      else if (responseType == ERROR_CORRUPT_RESPONSE) {
        Serial.println("Bad CRC");
      } else {
        Serial.print("Unknown error");
      }
    }
  }

  nano.stopReading();

  int archCheck;
  if (day == 'm' || day == 'M') {
    archCheck = 5;
  } else if (day == 't' || day == 'T') {
    archCheck = 6;
  } else if (day == 'w' || day == 'W') {
    archCheck = 7;
  } else if (day == 'r' || day == 'R') {
    archCheck = 8;
  } else if (day == 'f' || day == 'F') {
    archCheck = 9;
  } else if (day == 's' || day == 'S') {
    archCheck = 10;
  } else if (day == 'n' || day == 'N') {
    archCheck = 11;
  }

  
  for (int i = 0; i < archiveCount; i++) {
    if (archive[i][archCheck] >= 65 && archive[i][archCheck] <= 90) {
      bool archMatch = false;
      for (int j = 0; j < caughtCount; j++) {
        for (int k = 0; k < 12; k++) {
          if (archive[i][k] != epcCaught[j][k]) {
            break;
          }
          if (k == 11) {
            archMatch = true;
          }
        }
        if (j == caughtCount - 1) {
          if (archMatch) {
            Serial.print("Match: ");
          } else {
            Serial.print("Missing: ");
          }
          for (int k = 0; k < 3; k++) {
            Serial.print(archive[i][k]);
          }
          Serial.println((int)archive[i][3]);
        }
      }
    }
  }
  Serial.println("End");  
}

void writeRFID(char entry[]) {
  Serial.println("Writing to RFID");
  
  byte responseType = nano.writeTagEPC(entry, 12);
  
  if (responseType == RESPONSE_SUCCESS)
    Serial.println("New EPC Written!");
  else
    Serial.println("Failed write");
}

void checkArchive() {
  for (int i = 0; i < archiveCount; i++) {
    for (int j = 0; j < 12; j++) {
      if (j == 3)
        Serial.print((int)archive[i][j]);
      else
        Serial.print(archive[i][j]);
    }
    Serial.println();
  }
}

boolean setupNano(long baudRate)
{
  nano.begin(softSerial); //Tell the library to communicate over software serial port
  softSerial.begin(baudRate); //For this test, assume module is already at our desired baud rate
  
  while (!softSerial); //Wait for port to open
  while (softSerial.available()) 
    softSerial.read();
  
  nano.getVersion();
  if (nano.msg[0] == ERROR_WRONG_OPCODE_RESPONSE)
  {
    nano.stopReading();
    Serial.println(F("Module continuously reading. Asking it to stop..."));
    delay(1500);
  }
  else
  {
    softSerial.begin(115200); //Start software serial at 115200
    nano.setBaud(baudRate); //Tell the module to go to the chosen baud rate. Ignore the response msg
    softSerial.begin(baudRate); //Start the software serial port, this time at user's chosen baud rate
  }

  nano.getVersion();
  if (nano.msg[0] != ALL_GOOD) 
    return (false); //Something is not right

  nano.setTagProtocol(); //Set protocol to GEN2
  nano.setAntennaPort(); //Set TX/RX antenna ports to 1
  return (true); //We are ready to rock
}
