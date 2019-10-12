#include <SoftwareSerial.h>
 
SoftwareSerial mySerial(2, 3); // RX, TX
char buffer[8] ;
void setup()  
{
  // Инициализируем последовательный интерфейс и ждем открытия порта:
  Serial.begin(38400);
  while (!Serial) {
    ; // ожидаем подключения к последовательному порту. Необходимо только для Leonardo
  }

  Serial.print("Hello");
 
  // устанавливаем скорость передачи данных для последовательного порта, созданного 
  // библиотекой SoftwareSerial
  mySerial.begin(38400);
 // mySerial.write("A");
}
 
void loop() // выполняется циклически
{

 mySerial.write("A");
 delay(5);

  for (int i=0; i<8; i++) 
  {
    buffer[i] = mySerial.read();   
  }

  Serial.print((uint8_t)buffer[0]); 
  Serial.write(" ");
  Serial.print((uint8_t)buffer[1]); 
  Serial.write(" ");
  Serial.print((uint8_t)buffer[2]); 
  Serial.write(" ");
  Serial.print((uint8_t)buffer[3]); 
  Serial.write(" ");
  Serial.write("\n");
  
  
  delay(80); 
}
