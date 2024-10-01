from tornado import websocket
from tornado.ioloop import IOLoop
import asyncio


# 定义异步函数
_server_ws_url = "ws://localhost:8888/api/v2/user"
async def main():
    asyncio.sleep(1)
    ws = await websocket.websocket_connect(_server_ws_url)
    await ws.write_message("我佛")



# def run():
#     for i in range(5):
#         loop.run_until_complete(main())
#
#
# loop = asyncio.get_event_loop()

if __name__ == "__main__":
    IOLoop.current().run_sync(main)

