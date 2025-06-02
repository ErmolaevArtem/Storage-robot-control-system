#include <WiFi.h>
#include <driver/i2s.h>

// Настройки Wi-Fi
const char* ssid = "LEO";
const char* password = "12345678";

// Настройки I2S
const i2s_port_t I2S_PORT = I2S_NUM_0;
// Pin definitions
#define I2S_WS 25
#define I2S_SD 33
#define I2S_SCK 26
#define BUTTON 15
#define LED_GREEN 14
#define LED_RED 12
#define LED_ERROR 27
const int SAMPLE_RATE = 16000;  // Частота дискретизации
const int BUFFER_SIZE = 1024;   // Размер буфера
const int PORT = 12345;         // Порт для передачи данных

WiFiServer server(PORT);

void setup() {
  Serial.begin(115200);

  pinMode(BUTTON, INPUT_PULLUP);
  pinMode(LED_GREEN, OUTPUT);
  digitalWrite(LED_GREEN, LOW);
  pinMode(LED_RED, OUTPUT);
  digitalWrite(LED_RED, LOW);
  pinMode(LED_ERROR, OUTPUT);
  digitalWrite(LED_ERROR, LOW);

  // Подключение к Wi-Fi
  WiFi.softAP(ssid, password);

  IPAddress IP = WiFi.softAPIP();
  Serial.print("AP IP address: ");
  Serial.println(IP);

  server.begin();
  WiFiClient client = server.available();

  // Настройка I2S
  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = SAMPLE_RATE,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_I2S,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 8,
    .dma_buf_len = BUFFER_SIZE,
    .use_apll = false
  };

  i2s_pin_config_t pins = {
    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,
    .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num = I2S_SD
  };

  i2s_driver_install(I2S_PORT, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_PORT, &pins);

  // Запуск сервера
  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    Serial.println("Клиент подключен");
    digitalWrite(LED_GREEN, HIGH);

    int16_t samples[BUFFER_SIZE];
    size_t bytes_read;

    String received = "";

    while (client.connected()) {
      while (!digitalRead(BUTTON)) {
        if (!digitalRead(LED_RED)) digitalWrite(LED_RED, HIGH);
        // Чтение данных с микрофона
        i2s_read(I2S_PORT, &samples, BUFFER_SIZE * sizeof(int16_t), &bytes_read, portMAX_DELAY);

        // Передача данных по Wi-Fi
        client.write((uint8_t*)samples, bytes_read);
      }
      if (digitalRead(LED_RED)) digitalWrite(LED_RED, LOW);

      char c = client.read();
      if (c == 110) {
        digitalWrite(LED_ERROR, HIGH);
        delay(2000);
        digitalWrite(LED_ERROR, LOW);
      }

    }

    client.stop();
    Serial.println("Клиент отключен");
    digitalWrite(LED_GREEN, LOW);
  }
}