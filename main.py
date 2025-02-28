import discord
import pyaudio
import wave
import random
import time
import speech_recognition as sr
import os
import pyttsx3
from pydub import AudioSegment
from pydub.effects import speedup, low_pass_filter
from discord.ext import commands
import asyncio

TOKEN = "YOUR_BOT_TOKEN"
intents = discord.Intents.default()
intents.voice_states = True
intents.messages = True
intents.guilds = True
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

voice_client = None
recognizer = sr.Recognizer()
user_voice_data = {}

def generate_ghost_name():
    """Generates a random ghost name."""
    ghost_names = [
        "Elias Moreno", "Margaret Smith", "Samuel Dupont", "Isabella Rossi", "Jonathan Lee", "Lucille Yamamoto",
        "Victor Kowalski", "Catherine O'Connor",
        "Hugo Fernández", "Nina Petrov", "Lars Johansson", "Sophie Müller", "Javier Alvarez", "Anya Ivanova",
        "Omar El-Masri", "Mei Ling", "Diego Santos", "Aiko Nakamura",
        "Raphael Costa", "Elena Dimitrova", "Alejandro Pérez", "Hassan Benali", "Yuki Takahashi", "Fatima Hassan",
        "Carlos Ortega", "Ludwig Schneider", "Selena González"
    ]
    return random.choice(ghost_names)

def ghost_response():
    """Simulates a ghostly response with varied and intelligent phrases."""
    responses = [
        "I am here...", "Do not call me...", "Darkness surrounds us...",
        "Leave...", "I am trapped...", "Listen carefully...",
        "I am not alone...", "Fear...", "The energy is strong...",
        "Why have you summoned me?", "Time is an illusion...", "Do not trust the shadows...",
        "The walls have ears...", "Cold follows me...", "Someone else is here...",
        "I am watching you from the other side...", "The portal is opening...", "Do you feel that in the air?",
        "Not everyone can see me...", "The truth is hidden...", "The afterlife is closer than you think..."
    ]
    return random.choice(responses)

def distort_voice(text, filename="ghost_voice.wav"):
    """Converts text into distorted ghostly voice audio."""
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 100)  # Reduce speed
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)
        engine.save_to_file(text, filename)
        engine.runAndWait()

        sound = AudioSegment.from_file(filename)
        sound = low_pass_filter(sound, 500)  # Low-pass filter
        sound = speedup(sound, playback_speed=0.8)  # Reduce speed
        sound.export(filename, format="wav")
    except Exception as e:
        print(f"Error in distort_voice: {e}")

@bot.command()
async def summon(ctx):
    """Command to make the bot join the user's voice channel."""
    global voice_client
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice_client = await channel.connect()
        await ctx.send("👻 I have joined the voice channel. The spirit session begins...")
    else:
        await ctx.send("❌ You are not in a voice channel.")

@bot.command()
async def leave(ctx):
    """Command to make the bot leave the voice channel."""
    global voice_client
    if voice_client:
        await voice_client.disconnect()
        voice_client = None
        await ctx.send("👋 Closing connection with the beyond...")
    else:
        await ctx.send("❌ I am not in a voice channel.")

async def recognize_audio():
    """Captures and transcribes audio from the voice call."""
    try:
        with sr.Microphone() as source:
            print("🎤 Listening in the voice call...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language="en-US")
            return text
    except sr.UnknownValueError:
        return "(Nothing was understood)"
    except sr.RequestError:
        return "(Recognition error)"
    except Exception as e:
        print(f"Error in recognize_audio: {e}")
        return "(Error capturing audio)"

@bot.command()
async def listen(ctx):
    """Listens to what users say in the voice call and responds."""
    global voice_client
    if not voice_client:
        await ctx.send("❌ I am not in a voice channel. Use !summon first.")
        return

    await ctx.send("🎙️ Listening to the conversation in the call...")
    while True:
        heard_text = await recognize_audio()
        if heard_text and heard_text != "(Error capturing audio)":
            user = ctx.author.name  # Identify the user who spoke
            if user not in user_voice_data:
                user_voice_data[user] = generate_ghost_name()
            ghost_name = user_voice_data[user]

            await ctx.send(f"🗣️ {user} said: {heard_text}")
            response = ghost_response()
            await ctx.send(f"👁️ {ghost_name}: {response}")
            distort_voice(response)
            if os.path.exists("ghost_voice.wav"):
                source = discord.FFmpegPCMAudio("ghost_voice.wav")
                if not voice_client.is_playing():
                    voice_client.play(source)
        await asyncio.sleep(5)

bot.run(TOKEN)