from driver import Driver
from aiohttp import web
from config import Config 
from urllib import parse
import random 
import aiofiles

async def handle_asset(request):
	method = request.method

	try:
		if method == "GET":
			data = request.query 
			filepath = data["file"]

			async with aiofiles.open(Config.ASSETS + filepath, 'rb') as f:
				response = web.StreamResponse(status=200, reason='OK')
				response.content_type = 'application/octet-stream'
				await response.prepare(request)

				while True:
					chunk = await f.read(1024)
					if not chunk:
						break
					await response.write(chunk) 

				await response.write_eof()
				return response

		elif method == "PUT":
			reader = await request.multipart()
			field = await reader.next()

			alphabet = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
			filepath = ''.join(random.choice(alphabet) for i in range(30)) + '.' + field.filename.split('.')[-1]

			async with aiofiles.open(Config.ASSETS + filepath, 'wb') as f:
				while True:
					chunk = await field.read_chunk()
					if not chunk:
						break
					await f.write(chunk)

			return web.Response(text=filepath, status=200)
	except:
		return web.Response(status=400)

async def handle_user(request):
	try:
		method = request.method
		data = await request.json()

		if method == "POST":
			data = await Driver.select(data, "users")
			return web.json_response(data)
		elif method == "PUT":
			await Driver.insert(data, "users")
			return web.Response(status=200)
		elif method == "PATCH":
			await Driver.update(data, "users")
			return web.Response(status=200)
		elif method == "DELETE":
			await Driver.delete(data, "users")
			return web.Response(status=200)
		else:
			return web.Response(status=405)
	except:
		return web.Response(status=400)

async def handle_chat(request):
	try:
		method = request.method
		data = await request.json() 

		if method == "POST":
			data = await Driver.select(data, "chats")
			return web.json_response(data)
		elif method == "PUT":
			await Driver.insert(data, "chats")
			return web.Response(status=200)
		elif method == "PATCH":
			await Driver.update(data, "chats")
			return web.Response(status=200)
		elif method == "DELETE":
			await Driver.delete(data, "chats")
			return web.Response(status=200)
		else:
			return web.Response(status=405)
	except:
		return web.Response(status=400)

async def handle_message(request):
	try:
		method = request.method
		data = await request.json() 

		if method == "POST":
			data = await Driver.select(data, "messages")
			return web.json_response(data)
		elif method == "PUT":
			await Driver.insert(data, "messages")
			return web.Response(status=200)
		elif method == "PATCH":
			await Driver.update(data, "messages")
			return web.Response(status=200)
		elif method == "DELETE":
			await Driver.delete(data, "messages")
			return web.Response(status=200)
		else:
			return web.Response(status=405)
	except:
		return web.Response(status=400)
