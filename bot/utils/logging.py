import betterlogging as logging


def load_logging_handlers(logger) -> None:
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("bot/logging/warnings.log")
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(
        logging.Formatter(
            "%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s"
        )
    )

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
