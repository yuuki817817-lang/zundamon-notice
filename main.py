import os
import discord

intents = discord.Intents.default()
intents.voice_states = True

client = discord.Client(intents=intents)

ZUNDAMON_ID = 917633605684056085

# サーバーIDと、そのサーバー用の通知チャンネルIDを紐付ける辞書
SERVER_CHANNEL_MAP = {
    1486792533404291084: 1564663821161865267,  # 1つ目のサーバー
    1545825944797843496: 1564676976630046911,  # 2つ目のサーバー
}

@client.event
async def on_ready():
    print(f'通知Bot ({client.user}) が正常に起動したのだ！')

@client.event
async def on_voice_state_update(member, before, after):
    # デバッグ用のログ（Discordの動きをキャッチできているか確認用）
    print(f"【デバッグ】音声の動きを検知しました！ メンバーID: {member.id}")

    if member.id != ZUNDAMON_ID:
        return

    # 今イベントが起きたサーバー（ギルド）を特定する
    guild = after.guild if after.guild else before.guild
    if guild.id not in SERVER_CHANNEL_MAP:
        return

    # そのサーバー専用のチャンネルIDを取り出す
    channel_id = SERVER_CHANNEL_MAP[guild.id]
    channel = client.get_channel(channel_id)
    if channel is None:
        return

    # それぞれのサーバー専用のチャンネルに通知を送る
    if before.channel != after.channel and after.channel is not None:
        await channel.send(f"🔴 **【使用中】** ずんだもんが **{after.channel.name}** に入室したのだ！")

    elif before.channel is not None and after.channel is None:
        await channel.send(f"🟢 **【空き】** ずんだもんが退室したのだ！使っても大丈夫なのだ！")

import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

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

client.run(os.environ['DISCORD_TOKEN'])
