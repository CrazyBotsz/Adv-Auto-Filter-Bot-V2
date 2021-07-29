import time
from bot import CHAT_DETAILS

def time_formatter(seconds: float) -> str:
    """ 
    humanize time 
    """
    minutes, seconds = divmod(int(seconds),60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s") if seconds else "")
    return tmp


async def admin_list(chat_id, bot, update):
    """
    Creates A List Of Admin User ID's
    """
    global CHAT_DETAILS
    admins_id_list = []
    async for x in bot.iter_chat_members(chat_id=chat_id, filter="administrators"):
        admin_id = x.user.id 
        admins_id_list.append(admin_id)
    
    admins_id_list.append(None)
    CHAT_DETAILS[str(chat_id)] = dict(admins = admins_id_list)
    return admins_id_list