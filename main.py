import aiohttp
from aiohttp import web
from config import Config
from driver import Driver
from api import handle_asset
from api import handle_user
from api import handle_message
from api import handle_chat

app = web.Application()
app.add_routes([
	web.route('*', "/user", handle_user),
	web.route('*', "/chat", handle_chat),
	web.route('*', "/message", handle_message),
	web.route('*', "/asset", handle_asset)
])

if __name__ == '__main__':
	if Config.DB_INIT == True:
		Driver.initialize()

	web.run_app(app, port=Config.PORT)
