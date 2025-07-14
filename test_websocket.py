import asyncio
import websockets

async def test_websocket():
    uri = "ws://localhost:8000/ws/progress/"
    async with websockets.connect(uri) as websocket:
        message = input("Enter message to send: ")
        await websocket.send(message)
        print(f"> Sent: {message}")

        response = await websocket.recv()
        print(f"< Received: {response}")

asyncio.run(test_websocket())
