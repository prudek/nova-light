idf_component_register(
    SRCS "src/console_cli.c"
    INCLUDE_DIRS "include"
    REQUIRES console
    PRIV_REQUIRES esp_app_format
)
