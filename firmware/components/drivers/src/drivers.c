#include "drivers.h"
#include "esp_log.h"

static const char *TAG = "drivers";

esp_err_t drivers_init(void)
{
    ESP_LOGI(TAG, "Low-level peripheral drivers behind stable abstractions.");
    return ESP_OK;
}
