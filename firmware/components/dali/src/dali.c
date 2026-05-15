#include "dali.h"
#include "esp_log.h"

static const char *TAG = "dali";

esp_err_t dali_service_init(void)
{
    ESP_LOGI(TAG, "DALI protocol abstraction and future integration point.");
    return ESP_OK;
}
