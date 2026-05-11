from logger_config import validation_logger


REQUIRED_FIELDS = [
    "id",
    "nomeCivil"
]


def validar_deputado(data):
    if not data:
        validation_logger.error(
            "Empty object"
        )

        return False

    for field in REQUIRED_FIELDS:
        if field not in data or not data[field]:
            validation_logger.error(
                f"Missing field: {field} on ID={data.get('id')}"
            )

            return False
    validation_logger.info("complete")
    return True