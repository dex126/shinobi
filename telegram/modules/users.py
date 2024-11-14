import json
from datetime import timedelta

from telegram.modules import user_info
from telegram.utils import db


def render_info(info: user_info.ParsedUserInfo) -> tuple[bool, str | None]:
    return(info.is_pinned, info.group)


async def add_user(id: int, is_pinned: bool, group: str | None) -> bool:
    try:
        await db.users_db.setex(name=f"id:{id}", value=json.dumps(
                {
                    "is_pinned": is_pinned,
                    "group": group,
                }
                ),
                time=timedelta(days=365)
            )
        
        return(is_pinned, group)
    
    except:
        return False
    

async def user_credentials(id: int) -> list[dict]:
    found_records = [
        item async for item in db.users_db.scan_iter(f"id:{id}")
    ]

    record_values = map(
        json.loads, await db.users_db.mget(found_records)
    )

    return list(record_values)


async def parse_user_credentials(id: int) -> tuple[bool, str | None] | None:
    user_init = user_info.UserInfo(id=id)

    try:
        pullout_info = await user_init.get_user_info()

        human_data = render_info(pullout_info[0])

        return human_data
    
    except IndexError:
        new_user = await add_user(id=id,
                       is_pinned=False,
                       group=None)
        
        return(new_user)
