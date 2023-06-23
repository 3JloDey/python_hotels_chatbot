from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot) -> None:
    """
    Set the bot's commands.

    Args:
        bot (Bot): The bot instance to set the commands for.

    Returns:
        None

    """
    commands = [
        BotCommand(command="start", description="Start Bot"),
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
