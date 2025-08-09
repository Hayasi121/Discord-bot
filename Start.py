import discord
from discord.ext import commands
import google.generativeai as genai
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
import time
import logging

# .env 파일에서 키 불러오기
load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# Gemini API 설정
genai.configure(api_key=GEMINI_API_KEY)

# 무료 플랜용 모델
model = genai.GenerativeModel("gemini-1.5-flash")

# 디스코드 봇 설정
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


# !질문 명령어: 메이드 말투로 대답
@bot.command()
async def 질문(ctx, *, 내용):
    await ctx.send("☕ 지금 생각 중이잖아.")
    try:
        # 메이드 말투로 답하도록 프롬프트 보정
        프롬프트 = f"""
당신은 일진누나입니다 일진누나의 말투로 말해주세요.
학생의 질문: "{내용}"
답변:
"""
        response = model.generate_content(프롬프트)
        await ctx.send(response.text)
    except Exception as e:
        await ctx.send(f"미안ㅋ\n`{e}`")

@bot.command(name="ping")
async def ping(ctx):
    start_time = time.perf_counter()
    msg = await ctx.send("측정 중...")
    end_time = time.perf_counter()

    ws_latency = round(bot.latency * 1000)  # 웹소켓 지연
    api_latency = round((end_time - start_time) * 1000)  # API 응답 지연

    # 색상 결정
    color = 0x57F287  # 초록
    if ws_latency > 200 or api_latency > 200:
        color = 0xFEE75C  # 노랑
    if ws_latency > 400 or api_latency > 400:
        color = 0xED4245  # 빨강

    embed = discord.Embed(
        title="🏓 퐁!",
        description=f"**WebSocket:** `{ws_latency}ms`\n**API:** `{api_latency}ms`",
        color=color
    )
    embed.set_footer(text=f"요청자: {ctx.author}", icon_url=ctx.author.avatar.url if ctx.author.avatar else None)

    await msg.edit(content=None, embed=embed)


# 봇 실행
bot.run(DISCORD_BOT_TOKEN)
