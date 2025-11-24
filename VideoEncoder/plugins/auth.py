

from pyrogram import Client, filters

from .. import EVERYONE_CHATS, SUDO_USERS
from ..utils.database.access_db import db
from ..utils.helper import check_chat, output


@Client.on_message(filters.command('addchat'))
async def addchat(client, message):
    c = await check_chat(message, chat='OWNER_ID')
    if not c:
        return
    user_id = get_id(message)
    auth = await db.get_chat()
    if user_id in EVERYONE_CHATS:
        await reply_already_auth(message)
        return
    elif str(user_id) in auth:
        await reply_already_auth(message)
        return
    else:
        auth += ' ' + str(user_id)
        await db.set_chat(auth)
        await message.reply_text('Added to auth chats! ID: <code>{}</code>'.format(user_id))


@Client.on_message(filters.command('addsudo'))
async def addsudo(client, message):
    c = await check_chat(message, chat='OWNER_ID')
    if not c:
        return
    user_id = get_id(message)
    auth = await db.get_sudo()
    if user_id in SUDO_USERS:
        await reply_already_auth(message)
        return
    elif str(user_id) in auth:
        await reply_already_auth(message)
        return
    else:
        auth += ' ' + str(user_id)
        await db.set_sudo(auth)
        await message.reply_text('Added to sudo chats! ID: <code>{}</code>'.format(user_id))


@Client.on_message(filters.command('rmchat'))
async def rmchat(client, message):
    c = await check_chat(message, chat='OWNER_ID')
    if not c:
        return
    user_id = get_id(message)
    check = await db.get_chat()
    if str(user_id) in check:
        user_id = ' ' + str(user_id)
        auth = check.replace(user_id, '')
        await db.set_chat(auth)
        await message.reply_text('Removed from auth chats! ID: <code>{}</code>'.format(user_id))
        return
    elif user_id in EVERYONE_CHATS:
        await message.reply_text('Config auth removal not supported (To Do)!')
        return
    else:
        await message.reply_text('Chat is not auth yet!')


@Client.on_message(filters.command('rmsudo'))
async def rmsudo(client, message):
    c = await check_chat(message, chat='OWNER_ID')
    if not c:
        return
    user_id = get_id(message)
    check = await db.get_sudo()
    if str(user_id) in check:
        user_id = ' ' + str(user_id)
        auth = check.replace(user_id, '')
        await db.set_sudo(auth)
        await message.reply_text('Removed from sudo chats! ID: <code>{}</code>'.format(user_id))
        return
    elif user_id in EVERYONE_CHATS:
        await message.reply_text('Config sudo removal not supported (To Do)!')
        return
    else:
        await message.reply_text('Chat is not auth yet!')


async def reply_already_auth(message):
    if message.reply_to_message:
        await message.reply(text='They are already in auth users...')
        return
    elif not message.reply_to_message and len(message.command) != 1:
        await message.reply(text='They are already in auth users/group...')
        return
    else:
        await message.reply(text='This chat is already in auth users/groups...')
        return


def get_id(message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    elif not message.reply_to_message and len(message.command) != 1:
        user_id = message.text.split(None, 1)[1]
    else:
        user_id = message.chat.id
    return user_id
