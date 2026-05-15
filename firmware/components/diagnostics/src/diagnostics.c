#include "diagnostics.h"
#include "esp_log.h"

static const char *TAG = "diagnostics";

esp_err_t diagnostics_log_boot_banner(void)
{
    ESP_LOGI(TAG, "Logging, health reporting, reset reason, and diagnostic helpers.");
    return ESP_OK;
}
