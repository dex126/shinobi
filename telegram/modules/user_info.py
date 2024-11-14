from dataclasses import dataclass

from telegram.modules import users


@dataclass
class ParsedUserInfo:
    is_pinned: bool
    group: str | None


class UserInfo:
    def __init__(self, id: int) -> None:
        self.id = id


    async def get_user_info(self) -> list[ParsedUserInfo]:
        parsed_info = sorted(
            [   
                ParsedUserInfo(**info)
                for info in await users.user_credentials(self.id)
            ],
        )

        return parsed_info