from handlers import start, handle_message, info, bot, dp
import asyncio


async def main():
    await asyncio.gather(
        dp.start_polling(bot),
    )

#https:/t.me/ILEsistem_bot
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass