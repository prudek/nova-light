#include "connectivity.h"
#include "esp_log.h"

static const char *TAG = "connectivity";

esp_err_t connectivity_start(void)
{
    ESP_LOGI(TAG, "Wi-Fi, BLE, Ethernet, MQTT, and HTTP service orchestration.");
    return ESP_OK;
}
