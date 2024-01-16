from config import Config
import aiosqlite
import sqlite3 as sqlite

class Driver:
	@staticmethod
	def initialize():
		tables = [item.strip() for item in Config.DB_TEMPLATE.split("---")]
		
		with sqlite.connect(Config.DB) as conn:
			cursor = conn.cursor()
			for table in tables:
				cursor.execute(table)
			conn.commit()

	@staticmethod
	def forge_query(method, data, table):
		try:
			for key, value in data["id"].items():
				if type(data["id"][key]) == str:
					data["id"][key] = f"'{value}'"
		except:
			pass

		try:
			for key, value in data["spec"].items():
				if type(data["spec"][key]) == str:
					data["spec"][key] = f"'{value}'"
		except:
			pass

		suffix = ""
		if data.get("union", False):
			suffix = " OR (" + " AND ".join([f"`{key}`={value}" for key, value in data["id1"].items()]) + ")"
		if method == "select":
			return f"SELECT {', '.join(f'`{i}`' for i in data['spec'].split())} FROM {table} WHERE (" + " AND ".join([f"`{key}`={value}" for key, value in data["id"].items()]) + ") " + suffix
		elif method == "update":
			return f"UPDATE {table} SET " + ", ".join([f"`{key}`={value}" for key, value in data["spec"].items()]) + \
				" WHERE (" + " AND ".join([f"`{key}`={value}" for key, value in data["id"].items()]) + ") " + suffix
		elif method == "delete":
			return f"DELETE FROM {table} WHERE (" + " AND ".join([f"`{key}`={value}" for key, value in data["id"].items()]) + ") " + suffix 
		elif method == "insert":
			return f"INSERT INTO {table}(" + ", ".join([f"`{key}`" for key in data["spec"].keys()]) + \
				") VALUES (" + ", ".join([f"{value}" for value in data["spec"].values()]) + ")"

	@staticmethod
	async def select(data, table):
		query = Driver.forge_query("select", data, table)
		rows = []

		async with aiosqlite.connect(Config.DB) as conn:
			async with conn.cursor() as cursor:
				await cursor.execute(query)
				rows = await cursor.fetchall()

		ret = []
		for row in rows:
			ret.append(dict((key, value) for key, value in zip(data["spec"].split(), row)))
		return ret

	@staticmethod
	async def update(data, table):
		query = Driver.forge_query("update", data, table)

		async with aiosqlite.connect(Config.DB) as conn:
			async with conn.cursor() as cursor:
				await cursor.execute(query)
				await conn.commit()

	@staticmethod
	async def delete(data, table):
		query = Driver.forge_query("delete", data, table)

		async with aiosqlite.connect(Config.DB) as conn:
			async with conn.cursor() as cursor:
				await cursor.execute(query)
				await conn.commit()

	@staticmethod
	async def insert(data, table):
		query = Driver.forge_query("insert", data, table)

		async with aiosqlite.connect(Config.DB) as conn:
			async with conn.cursor() as cursor:
				await cursor.execute(query)
				await conn.commit()
