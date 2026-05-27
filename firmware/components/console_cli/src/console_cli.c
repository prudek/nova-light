#include "console_cli.h"

#include <inttypes.h>
#include <stdio.h>

#include "esp_app_desc.h"
#include "esp_console.h"
#include "esp_err.h"
#include "esp_log.h"
#include "esp_system.h"
#include "esp_timer.h"

static const char *TAG = "console_cli";
static esp_console_repl_t *s_repl = NULL;

static int cli_cmd_ping(int argc, char **argv)
{
    (void)argc;
    (void)argv;
    printf("pong\n");
    return 0;
}

static int cli_cmd_version(int argc, char **argv)
{
    (void)argc;
    (void)argv;
    const esp_app_desc_t *app_desc = esp_app_get_description();
    printf("%s\n", app_desc->version);
    return 0;
}

static int cli_cmd_status(int argc, char **argv)
{
    (void)argc;
    (void)argv;

    const esp_app_desc_t *app_desc = esp_app_get_description();
    const uint64_t uptime_seconds = esp_timer_get_time() / 1000000ULL;
    const uint32_t free_heap = esp_get_free_heap_size();
    const uint32_t min_free_heap = esp_get_minimum_free_heap_size();

    esp_chip_info_t chip_info;
    esp_chip_info(&chip_info);

    printf("version: %s\n", app_desc->version);
    printf("idf: %s\n", esp_get_idf_version());
    printf("cores: %d\n", chip_info.cores);
    printf("uptime_s: %" PRIu64 "\n", uptime_seconds);
    printf("heap_free: %" PRIu32 "\n", free_heap);
    printf("heap_min_free: %" PRIu32 "\n", min_free_heap);
    return 0;
}

static esp_err_t register_commands(void)
{
    const esp_console_cmd_t ping_cmd = {
        .command = "ping",
        .help = "Return pong",
        .hint = NULL,
        .func = &cli_cmd_ping,
    };
    esp_err_t err = esp_console_cmd_register(&ping_cmd);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to register ping command: %s", esp_err_to_name(err));
        return err;
    }

    const esp_console_cmd_t version_cmd = {
        .command = "version",
        .help = "Print firmware version",
        .hint = NULL,
        .func = &cli_cmd_version,
    };
    err = esp_console_cmd_register(&version_cmd);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to register version command: %s", esp_err_to_name(err));
        return err;
    }

    const esp_console_cmd_t status_cmd = {
        .command = "status",
        .help = "Print runtime status for release smoke checks",
        .hint = NULL,
        .func = &cli_cmd_status,
    };
    err = esp_console_cmd_register(&status_cmd);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to register status command: %s", esp_err_to_name(err));
        return err;
    }

    return ESP_OK;
}

esp_err_t console_cli_start(void)
{
    if (s_repl != NULL) {
        return ESP_OK;
    }

    esp_err_t err = esp_console_register_help_command();
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to register help command: %s", esp_err_to_name(err));
        return err;
    }

    err = register_commands();
    if (err != ESP_OK) {
        return err;
    }

    esp_console_repl_config_t repl_config = ESP_CONSOLE_REPL_CONFIG_DEFAULT();
    repl_config.prompt = "nova> ";
    repl_config.max_cmdline_length = 128;

    esp_console_dev_uart_config_t uart_config = ESP_CONSOLE_DEV_UART_CONFIG_DEFAULT();
    err = esp_console_new_repl_uart(&uart_config, &repl_config, &s_repl);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to initialize UART console REPL: %s", esp_err_to_name(err));
        return err;
    }

    err = esp_console_start_repl(s_repl);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "Failed to start UART console REPL: %s", esp_err_to_name(err));
        return err;
    }

    ESP_LOGI(TAG, "CLI started. Commands: help, version, ping, status");
    return ESP_OK;
}
