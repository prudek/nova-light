#include "app_core.h"
#include "esp_log.h"

static const char *TAG = "app_core";

esp_err_t app_core_start(void)
{
    ESP_LOGI(TAG, "Application orchestration and top-level lifecycle.");
    return ESP_OK;
}
