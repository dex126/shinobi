from aiogram.types import InputMediaPhoto
from aiogram import Router, types, F

from telegram import config, bot
from telegram.modules import users


router = Router()


@router.message(F.text == 'Расписание звонков')
async def pin_message(message: types.Message):
    media_group = []
    media_group.append(InputMediaPhoto(media=config.PHOTO_URL_MONDAY))
    media_group.append(InputMediaPhoto(media=config.PHOTO_URL_OTHER,
                                       caption='<a href="https://t.me/shinobi_leave_bot" '
                                       'target="_blank"><b>Расписание звонков и пар, '
                                       'удобные инструменты — все это в Shinobi!</b></a>'))

    photo = await message.answer_media_group(media=media_group,
                                             disable_notification=True)

    message_is_pinned = await users.parse_user_credentials(id=message.from_user.id)

    if not message_is_pinned[0]:
        await users.add_user(id=message.from_user.id,
                                is_pinned=True,
                                group=message_is_pinned[1],
                                )

        for item in str(photo[0]).split(" "):
            if item.startswith("message_id"):
                await bot.bot.pin_chat_message(chat_id=message.from_user.id,
                                                message_id=item.split("=")[1])