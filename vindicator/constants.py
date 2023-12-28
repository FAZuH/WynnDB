from typing import Optional


__version__: str = "0.0.1"
API_KEY: Optional[str] = None

FETCH_GUILD_INTERVAL: int = 30
FETCH_ONLINE_INTERVAL: int = 30
FETCH_PLAYER_INTERVAL: int = 30

DEVELOPER_DISCORD_ID: int = 257428751560867840


class DatabaseTables:
    GUILD_MAIN = "guild_main"
    GUILD_MAIN_INFO = "guild_main_info"
    GUILD_MEMBER = "guild_member"
    PLAYER_ACTIVITY = "player_activity"
    PLAYER_CHARACTER = "player_character"
    PLAYER_CHARACTER_INFO = "player_character_info"
    PLAYER_MAIN = "player_main"
    PLAYER_MAIN_INFO = "player_main_info"
    RAW_RESPONSES = "raw_responses"

class Webhooks:
    DATABASE_WEBHOOK: str = "https://discord.com/api/webhooks/1175107043649138799/rsGUi3EQ1p8FBYA9o59KrZ9NEGN8hFxy9Yx9X9kNrTGbKxD86XvRYp7wWcJ0hUkirxIp"
    ERROR_WEBHOOK: str = "https://discord.com/api/webhooks/1175107206136463480/r9P468IHTLYzDcdCd6jM4pAYjb-sDqCAY38davwv8HehRrBZ2fRplb4JeCzYqf7U6WMV"
    FETCH_GUILD_WEBHOOK: str = "https://discord.com/api/webhooks/1165646068659265657/J1-COoyU3l-ez4q0d3BG_wb-MoD7GOXWeyWXs6Qy_SqHKF9ecqrDGDZpGLlsO2H_G75S"
    FETCH_ONLINE_WEBHOOK: str = "https://discord.com/api/webhooks/1175279388670042162/ymcM1IbmcEVKLgznxBLVRfbiGQqnw18hvyM14VzV_FGA3QdJPE-Y9N6Twqrqmcj_nGtK"
    FETCH_PLAYER_WEBHOOK: str = "https://discord.com/api/webhooks/1165645953462706266/AoIOMYmY9pdP8kCWqNFjjBZjCPGmVVeuSqoOjexi2mKbNSCBubGw5nRcP_EiARxWBK-T"
    WYNNCRAFT_REQUEST_WEBHOOK: str = "https://discord.com/api/webhooks/1185935055453945918/X0cgZ9H6jSm5tDbS1w1XXJ7s7xJD2e7Ng7ZqWQUJuIK-2oTRxoyQfFxuPK2eoYxbNC4O"