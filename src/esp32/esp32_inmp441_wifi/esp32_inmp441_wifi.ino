#include <WiFi.h>
#include <driver/i2s.h>

const char* ssid = "access_point2";
const char* password = "12345678";
const char* host = "10.42.0.1";  // IP ПК
const uint16_t port = 12345;

// Настройки I2S
#define I2S_WS 25
#define I2S_SD 33
#define I2S_SCK 26

#define SAMPLE_RATE 16000
#define I2S_BUFFER_SIZE (16 * 1024)

WiFiClient client;

void setupI2S() {
  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = SAMPLE_RATE,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_I2S_MSB,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 4,
    .dma_buf_len = 512,
    .use_apll = false
  };

  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SCK,
    .ws_io_num = I2S_WS,
    .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num = I2S_SD
  };

  i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
  i2s_set_pin(I2S_NUM_0, &pin_config);
}

void i2s_adc_data_scale(uint8_t* d_buff, uint8_t* s_buff, uint32_t len) {
  uint32_t j = 0;
  uint32_t dac_value = 0;
  for (int i = 0; i < len; i += 2) {
    dac_value = ((((uint16_t)(s_buff[i + 1] & 0xf) << 8) | ((s_buff[i + 0]))));
    d_buff[j++] = 0;
    d_buff[j++] = dac_value * 256 / 2048;
  }
}

void setup() {
  pinMode(15, INPUT_PULLUP);
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("Connected.");

  setupI2S();

  Serial.print("Connecting to server...");
  while (!client.connect(host, port)) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("Connected to server.");
  

  // xTaskCreate(&recording_task, "snd_task", 32000, NULL, 5, NULL);
}

// static uint8_t i2s_data[I2S_BUFFER_SIZE];
// static uint8_t i2s_adc_data[I2S_BUFFER_SIZE];
// size_t bytes_read;
bool recording = 1;

void loop() {
  if((!digitalRead(15)) && (recording)){
    recording = 0;
    xTaskCreate(&recording_task, "snd_task", 32000, NULL, 5, NULL);
  }

  // i2s_read(I2S_NUM_0, &i2s_data, I2S_BUFFER_SIZE, &bytes_read, portMAX_DELAY);
  // i2s_adc_data_scale(i2s_adc_data, i2s_data, I2S_BUFFER_SIZE);
  // if (bytes_read > 0 && client.connected()) {
  //   client.write(i2s_adc_data, I2S_BUFFER_SIZE);
  // }
}

void recording_task(void *param) {
  static uint8_t i2s_data[I2S_BUFFER_SIZE];
  static uint8_t i2s_adc_data[I2S_BUFFER_SIZE];
  size_t bytes_read;
  int counter = 0;
  Serial.print("Starting in 3...");
  delay(1000);
  Serial.print("2...");
  delay(1000);
  Serial.println("1...");
  delay(1000);
  Serial.println("Started");
  while (1) {
    i2s_read(I2S_NUM_0, &i2s_data, I2S_BUFFER_SIZE, &bytes_read, portMAX_DELAY);
    i2s_adc_data_scale(i2s_adc_data, i2s_data, I2S_BUFFER_SIZE);
    if (bytes_read > 0 && client.connected()) {
      client.write(i2s_adc_data, I2S_BUFFER_SIZE);
      counter++;
    }
    if(counter >= 8){
      recording = 1;
      Serial.println("Finished");
      vTaskDelete(NULL);
    }
  }
}
