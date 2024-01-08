from driver import Driver
from aiohttp import web
from config import Config 
import random 
import aiofiles

async def handle_asset(request):
	method = request.method

	try:
		if method == "GET":
			data = await request.json() 
			filepath = data["file"]

			async with aiofiles.open(filepath, 'rb') as f:
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

		elif method == "POST":
			reader = await request.multipart()
			field = await reader.next()

			alphabet = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
			filepath = Config.ASSETS + ''.join(random.choice(alphabet) for i in range(30)) + '.' + field.filename.split('.')[-1]

			async with aiofiles.open(filepath, 'wb') as f:
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

		if method == "GET":
			data = await Driver.select(data, "users")
			return web.json_response(data)
		elif method == "POST":
			await Driver.insert(data, "users")
			return web.Response(status=200)
		elif method == "PUT":
			await Driver.update(data, "users")
			return web.Response(status=200)
		elif method == "DELETE":
			await Driver.delete(data, "users")
			return web.Response(status=200)
		else:
			return web.Response(status=405)
	except:
		return web.Response(status=400)

async def handle_follower(request):
	try:
		method = request.method
		data = await request.json() 

		if method == "GET":
			data = await Driver.select(data, "followers")
			return web.json_response(data)
		elif method == "POST":
			await Driver.insert(data, "followers")
			return web.Response(status=200)
		elif method == "PUT":
			await Driver.update(data, "followers")
			return web.Response(status=200)
		elif method == "DELETE":
			await Driver.delete(data, "followers")
			return web.Response(status=200)
		else:
			return web.Response(status=405)
	except:
		return web.Response(status=400)

async def handle_message(request):
	try:
		method = request.method
		data = await request.json() 

		if method == "GET":
			data = await Driver.select(data, "messages")
			return web.json_response(data)
		elif method == "POST":
			await Driver.insert(data, "messages")
			return web.Response(status=200)
		elif method == "PUT":
			await Driver.update(data, "messages")
			return web.Response(status=200)
		elif method == "DELETE":
			await Driver.delete(data, "messages")
			return web.Response(status=200)
		else:
			return web.Response(status=405)
	except:
		return web.Response(status=400)
