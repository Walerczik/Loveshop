from aiogram import Dispatcher
from . import admin, user

def register_handlers(dp: Dispatcher):
    admin.register_admin(dp)
    user.register_user(dp)
