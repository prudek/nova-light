#include "app_core.h"
#include "console_cli.h"
#include "diagnostics.h"
#include "esp_err.h"
#include "esp_log.h"

static const char *TAG = "main";

void app_main(void)
{
    ESP_LOGI(TAG, "Starting ESP32 agent-ready firmware baseline");
    const esp_err_t diagnostics_err = diagnostics_log_boot_banner();
    if (diagnostics_err != ESP_OK) {
        ESP_LOGE(TAG, "Diagnostics initialization failed: %s", esp_err_to_name(diagnostics_err));
        return;
    }

    const esp_err_t app_core_err = app_core_start();
    if (app_core_err != ESP_OK) {
        ESP_LOGE(TAG, "App core startup failed: %s", esp_err_to_name(app_core_err));
        return;
    }

    const esp_err_t cli_err = console_cli_start();
    if (cli_err != ESP_OK) {
        ESP_LOGE(TAG, "Console CLI startup failed: %s", esp_err_to_name(cli_err));
        return;
    }
}
