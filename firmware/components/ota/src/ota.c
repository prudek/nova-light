#include "ota.h"
#include "esp_log.h"

static const char *TAG = "ota";

esp_err_t ota_service_init(void)
{
    ESP_LOGI(TAG, "OTA update flow, manifest validation, rollback, and release traceability.");
    return ESP_OK;
}
