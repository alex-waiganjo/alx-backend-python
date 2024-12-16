import asyncio
import aiosqlite

DatabaseConnection = __import__('0-databaseconnection').DatabaseConnection

DATABASE = 'users.db'


async def async_fetch_users():
   
    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute("SELECT * FROM users")
        rows = await cursor.fetchall()
        await cursor.close()
        return rows
            

async def async_fetch_older_users():

    async with aiosqlite.connect(DATABASE) as db:
        cursor = await db.execute("SELECT * FROM users WHERE age > 40")
        rows = await cursor.fetchall()
        await cursor.close()
        return rows
    
    
async def fetch_concurrently():
   
    all_users, older_users = await asyncio.gather(async_fetch_users(), async_fetch_older_users())
    print(f"All users: {all_users}")
    print(f"Older users (age > 40): {older_users}")
    
    
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())