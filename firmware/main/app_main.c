#include "app_core.h"
#include "diagnostics.h"
#include "esp_log.h"

static const char *TAG = "main";

void app_main(void)
{
    ESP_LOGI(TAG, "Starting ESP32 agent-ready firmware baseline");
    diagnostics_log_boot_banner();
    app_core_start();
}
