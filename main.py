import os
import discord

intents = discord.Intents.default()
intents.voice_states = True 

client = discord.Client(intents=intents)

# ★コピーした実際のID
ZUNDAMON_ID = 917633605684056085
ANNOUNCE_CHANNEL_ID = 1564663821161865267

@client.event
async def on_ready():
    print(f'通知Bot（{client.user}）が正常に起動したのだ！')

@client.event
async def on_voice_state_update(member, before, after):
    if member.id != ZUNDAMON_ID:
        return

    channel = client.get_channel(ANNOUNCE_CHANNEL_ID)
    if channel is None:
        return

    if before.channel != after.channel and after.channel is not None:
        await channel.send(f"🔴 **【使用中】** ずんだもんが **{after.channel.name}** に入室したのだ！")
        
    elif before.channel is not None and after.channel is None:
        await channel.send(f"🟢 **【空き】** ずんだもんが退室したのだ！使っても大丈夫なのだ！")

import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord

# --- 以下を追加 ---
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()
# ------------------

# (※ここから下は既存の client.run です)
client.run(os.environ['DISCORD_TOKEN'])
