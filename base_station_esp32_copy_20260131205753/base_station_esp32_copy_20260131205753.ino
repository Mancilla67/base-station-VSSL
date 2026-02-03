#include <esp_now.h>
#include <WiFi.h>

//VARIABLES
#define NUM_ROBOTS 5

// Direccion de broadcast
uint8_t broadcastAddress[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

// Estructura del dato a enviar (Igual que antes)
typedef struct struct_mensaje{
    int8_t x_robot_1;
    int8_t y_robot_1;

    int8_t x_robot_2;
    int8_t y_robot_2;

    int8_t x_robot_3;
    int8_t y_robot_3;

    int8_t x_robot_4;
    int8_t y_robot_4;

    int8_t x_robot_5;
    int8_t y_robot_5;
} struct_mensaje;

struct_mensaje mimensaje;
esp_now_peer_info_t peerInfo;

void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status){
  // Opcional: Descomentar para debug, pero ensucia el monitor si mandas muy rapido
  // Serial.print("\r\nEstado: ");
  // Serial.println(status == ESP_NOW_SEND_SUCCESS ? "OK" : "Error");
}

void setup() {
  Serial.begin(115200); 
  WiFi.mode(WIFI_STA);

  if (esp_now_init() != ESP_OK) {
    Serial.println("Error inicializando ESP-NOW");
    return;
  }
  
  // Registrar Callback de envio
  esp_now_register_send_cb(OnDataSent);

  // Registrar Peer (Broadcast)
  memcpy(peerInfo.peer_addr, broadcastAddress, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;

  if (esp_now_add_peer(&peerInfo) != ESP_OK){
    Serial.println("Fallo al agregar el peer de Broadcast");
    return;
  }
}

void loop() {
  // ESPERAMOS FORMATO: "ID,X,Y\n"  (Ejemplo: "1,50,100")
  
  if(Serial.available() > 0){
    String data = Serial.readStringUntil('\n');
    
    // Buscamos las dos comas
    int firstComma = data.indexOf(',');
    int secondComma = data.indexOf(',', firstComma + 1);

    // Si encontramos las dos comas, procedemos
    if (firstComma > 0 && secondComma > 0){
      
      // 1. PARSEAR (Cortar el string en pedacitos)
      String idStr = data.substring(0, firstComma);
      String xStr  = data.substring(firstComma + 1, secondComma);
      String yStr  = data.substring(secondComma + 1);

      int id = idStr.toInt();
      int x  = xStr.toInt();
      int y  = yStr.toInt();

      // 2. LIMPIEZA DE SEGURIDAD (IMPORTANTE)
      // Ponemos toda la estructura en 0 antes de asignar.
      // Esto hace que si controlas el Robot 1, el 2, 3, 4 y 5 se frenen.
      //memset(&mimensaje, 0, sizeof(mimensaje));

      // 3. ASIGNAR VALORES AL ROBOT CORRESPONDIENTE
      switch (id) {
        case 1: 
          mimensaje.x_robot_1 = (int8_t)x; 
          mimensaje.y_robot_1 = (int8_t)y; 
          break;
        case 2: 
          mimensaje.x_robot_2 = (int8_t)x; 
          mimensaje.y_robot_2 = (int8_t)y; 
          break;
        case 3: 
          mimensaje.x_robot_3 = (int8_t)x; 
          mimensaje.y_robot_3 = (int8_t)y; 
          break;
        case 4: 
          mimensaje.x_robot_4 = (int8_t)x; 
          mimensaje.y_robot_4 = (int8_t)y; 
          break;
        case 5: 
          mimensaje.x_robot_5 = (int8_t)x; 
          mimensaje.y_robot_5 = (int8_t)y; 
          break;
      }

      // 4. ENVIAR A TODOS (Broadcast)
      esp_now_send(broadcastAddress, (uint8_t *) &mimensaje, sizeof(mimensaje));
    }
  }
}