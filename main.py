import discord
from discord import Embed
import pymysql
from discord.ext import commands
from datetime import datetime
import json
import os
import time


with open('./config.json') as f:
  data = json.load(f)
  print("Welcome to Yonatan Bot! Checking the config.json")
  for f in data['fivemConfig']:
      fivemsqlip = f['fivem-sql-ip']
      usersql = f['user-sql']
      passwordsql = f['password-sql']
      fivemsqldatabase = f['fivem-sql-database']
      fivemsqlquary = f['fivem-sql-quary']
  for c in data['botConfig']:
    os.system('color a')
    os.system('cls')
    if c['allowed_user'] == '0':
        os.system('color a')
        print("Make Sure the config is right! | allowed_user is invaild!")
        time.sleep(1)
        print("Exiting...")
        time.sleep(2)
        exit()
    elif c['token'] == 'token':
        os.system('color a')
        print("Make Sure the config is right! | token is invaild!")
        time.sleep(1)
        print("Exiting...")
        time.sleep(2)
        exit()
    else:
        print("Welcome to Yonatan Bot! Starting...")
        time.sleep(2)
        os.system('cls')
        os.system('color b')
        allowed_user = int(c['allowed_user'])
        token = c['token']
        servername = c['servername']


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!',intents=intents)
bot.remove_command('help')








@bot.command()
async def fivembans(ctx):
    if ctx.author.id == allowed_user:
        try:
            connection = pymysql.connect(
                host=fivemsqlip,
                user=usersql,
                password=passwordsql,
                db=fivemsqldatabase
            )

            cursor = connection.cursor()
            cursor.execute(f"SELECT * FROM {fivemsqlquary}")
            records = cursor.fetchall()

            embed_list = []

            embed = Embed(title=f"Banned Users | {servername}", color=0xff0000)

            field_count = 0

            for row in records:
                if field_count == 25:
                    embed_list.append(embed)
                    embed = Embed(title="List of Banned Users", color=0xff0000)
                    field_count = 0

                ts = row[6]
                finallol = datetime.fromtimestamp(ts)
                embed.add_field(name=f"({row[0]}) | " + row[1], value=f"Discord ID: `{row[3]}` | Reason: `{row[5]}` | Banned by: `{row[7]}` | Ban until: `{finallol}`", inline=False)
                embed.set_author(name="Made by Yonatan :)")
                embed.set_footer(text='Made by Yonatan :) | To unban someone, use - !fivemunban <ID>')
                field_count += 1

            embed_list.append(embed)

            for embed in embed_list:
                await ctx.send(embed=embed)
        except pymysql.Error as e:
            print("Error reading data from MySQL table", e)
        finally:
            if (connection.open):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
    else:
        await ctx.send("Sorry, You don't have permissions to use this adventure system.")





@bot.command()
async def fivemunban(ctx, id:int):
    if ctx.author.id == allowed_user:
        try:
            connection = pymysql.connect(
                host=fivemsqlip,
                user=usersql,
                password=passwordsql,
                db=fivemsqldatabase
            )

            cursor = connection.cursor()

            sql_query = f"DELETE FROM {fivemsqlquary} WHERE id = {id}"
            cursor.execute(sql_query)
            connection.commit()

            await ctx.send(f"User with ID {id} has been unbanned. to check that, write - `!fivembans`")
        except pymysql.Error as e:
            print("Error unbanning user", e)
        finally:
            if (connection.open):
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
    else:
        await ctx.send("Sorry, You don't have permissions to use this adventure system.")











bot.run(token)

