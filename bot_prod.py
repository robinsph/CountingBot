import aiocron
import asyncio
import datetime
import discord
from discord.ext import commands
from hashlib import sha256
import json
import math
from numpy import log as ln
import os
import random
import sqlalchemy as db
import time
from utils import generate_ban_time_string

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN_PROD')

'''
    Counting Bot Version 2.1.0
    Created: 2021-07-14
    Updated: 2021-07-25
    
    Phil Robinson
    Seattle, WA

    Counting Bot is a discord bot that manages specified text channels, making sure that users count in correct incrimental integers. 
    When a user submits a new input to the channel, Counting Bot checks what the current count of the the channel, determines if that input 
    will be timed out from the channel for an amount of time determined by the number of times that user has submitted and incorrect input.
    Lastly, Counting Bot will run a cron job every minute to determine if the timeout has expired. 

    NEW for Version 2.1.0
        - Created User Interface for intercting with database
        - Moved database off of NAS

    TODO for Version 2.1.1
        - Create interface for unbanning indefinite bans

    TODO for Version 2.2.0
        - Change from sqlite to Postgres SQL
            
'''

engine = db.create_engine("sqlite:///database_prod.db")
connection = engine.connect()
metadata = db.MetaData()
ban = db.Table('ban', metadata, autoload=True, autoload_with=engine)
input = db.Table('input', metadata, autoload=True, autoload_with=engine)
insult = db.Table('insult', metadata, autoload=True, autoload_with=engine)
permission = db.Table('permission', metadata, autoload=True, autoload_with=engine)
state = db.Table('state', metadata, autoload=True, autoload_with=engine)
user = db.Table('user', metadata, autoload=True, autoload_with=engine)


bot = commands.Bot(command_prefix='--')

@bot.event
async def on_ready():
    print(f"Online: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


@bot.event
async def on_message(message):
    query = db.select([permission.columns.CHANNEL_ID])
    result = connection.execute(query).fetchall()
    permitted_channels = [_.CHANNEL_ID for _ in result]

    if message.channel.id not in permitted_channels or message.author == bot.user:
        return

    query = db.select([state]).where(db.and_(
                                             state.columns.CHANNEL_ID == message.channel.id
                                            )
                                    )
    result = connection.execute(query).first()

    if result is None:
        query = db.insert(state)
        values = [{
                    'CHANNEL_ID': message.channel.id,
                    'CURRENT_STATE': 0,
                    'CREATE_DATE': datetime.datetime.now(),
                    'UPDATE_DATE': datetime.datetime.now()
                 }]
        connection.execute(query,values)
        current_value = 0
    else:
        current_value = result.CURRENT_STATE

    query = db.select([user]).where(db.and_(
                                            user.columns.DISCORD_ID == message.author.id,
                                            user.columns.CHANNEL_ID == message.channel.id
                                            )
                                    )
    result = connection.execute(query).first()

    if result is None:
        query = db.insert(user)
        values = [{
            'DISCORD_ID': message.author.id,
            'CHANNEL_ID': message.channel.id,
            'USER_NAME': message.author.name,
            'CREATE_DATE': datetime.datetime.now(),
            'UPDATE_DATE': datetime.datetime.now()
                 }]
        connection.execute(query,values)

        query = db.select([user]).where(db.and_(
                                            user.columns.DISCORD_ID == message.author.id,
                                            user.columns.CHANNEL_ID == message.channel.id
                                            )
                                    )
        result = connection.execute(query).first()
        user_id = result.USER_ID

    else:
        user_id = result.USER_ID
        user_name = result.USER_NAME
        if user_name != message.author.name:
            query = db.update(user).where(db.and_(
                                                    user.columns.DISCORD_ID == message.author.id,
                                                    user.columns.CHANNEL_ID == message.channel.id
                                                 )
                                        )
            values = [{
                        'USER_NAME': message.author.name,
                        'UPDATED': datetime.datetime.now()
                    }]
            connection.execute(query, values)


    if message.content.isnumeric() and int(message.content) - current_value == 1:
        correct = 1
        await message.add_reaction("✔️")
        
        query = db.select([state]).where(db.and_(
                                             state.columns.CHANNEL_ID == message.channel.id
                                            )
                                    )
        result = connection.execute(query).first()
        values = [{
                    'CURRENT_STATE': current_value + 1, 
                    'UPDATE_DATE': datetime.datetime.now()
                }]
        connection.execute(query, values)


    else:
        correct = 0
        await message.add_reaction("👎")

        skip_ban = False

        counting_admin = 867497301206892575
        if counting_admin in [role.id for role in message.author.roles]:
            skip_ban = True
        
        if skip_ban == False:
            await message.channel.set_permissions(message.author, send_messages=False)
            query = db.select([insult]).where(insult.columns.ACTIVE == 1).order_by(db.func.random())
            result = connection.execute(query).first()

            # if result.INSULT_TEXT is not None and result.INSULT_FILE != 'None':
                # await message.channel.send(content = result.INSULT_TEXT, file=discord.File(os.path.join('assets', result.INSULT_FILE)))
            if result.INSULT_TEXT != 'None':
                await message.channel.send(result.INSULT_TEXT)
            elif result.INSULT_FILE != 'None':
                await message.channel.send(file=discord.File(os.path.join('assets', result.INSULT_FILE)))

            if result.INDEFINITE_BAN == 0:
                '''
                    Ban function graph
                    https://www.desmos.com/calculator/6uvw2vrslv

                '''

                query = db.select([input]).where(db.and_(
                                                input.columns.USER_ID == user_id,
                                                input.columns.CORRECT_INPUT == 0
                                                )
                                        )
                result = connection.execute(query).fetchall()

                incorrect_inputs = len(result)

                ban_time = ((500/(1+math.e**(5+(-.45)*incorrect_inputs)))+0.25*incorrect_inputs)*3600
                ban_time = int(ban_time)

                unban_date = datetime.datetime.now() + datetime.timedelta(seconds=ban_time)

                query = db.insert(ban)
                values = [{ 'USER_ID': user_id,
                            'BAN_DATE': datetime.datetime.now(),
                            'UNBAN_DATE': unban_date,
                            'INDEFINITE_BAN': 0,
                            'CURRENTLY_BANNED': 1,
                            'CREATE_DATE': datetime.datetime.now(),
                            'UPDATE_DATE': datetime.datetime.now()
                        }]
                connection.execute(query, values)

                ban_string = generate_ban_time_string(ban_time)
                await message.channel.send(f"See you in {ban_string}!")
            else:
                query = db.insert(ban)
                values = [{ 'USER_ID': user_id,
                            'BAN_DATE': datetime.datetime.now(),
                            'UNBAN_DATE': None,
                            'INDEFINITE_BAN': 1,
                            'CURRENTLY_BANNED': 1,
                            'CREATE_DATE': datetime.datetime.now(),
                            'UPDATE_DATE': datetime.datetime.now()
                        }]
                connection.execute(query, values)


    '''
        log users input into the input table
    '''
    query = db.insert(input)
    values = [{
                'USER_ID': user_id, 
                'USER_INPUT': message.content, 
                'CORRECT_INPUT': correct,
                'CREATE_DATE': datetime.datetime.now()
            }]
    connection.execute(query, values)

    await bot.process_commands(message)

@aiocron.crontab('*/1 * * * *')
async def attime():
    query = db.select([ban]).where(db.and_(
                                            ban.columns.CURRENTLY_BANNED == 1,
                                            ban.columns.INDEFINITE_BAN == 0
                                          )
                                    )
    result = connection.execute(query).fetchall()
    for banned_user in result:
        date_difference = banned_user.UNBAN_DATE - datetime.datetime.now()
        seconds_difference = date_difference.total_seconds()
        if seconds_difference <= 0:
            banned_user_id = banned_user.USER_ID
            query = db.select([user]).where(user.columns.USER_ID == banned_user_id)
            interior_result = connection.execute(query).first()


            channel_id = await bot.fetch_channel(interior_result.CHANNEL_ID)
            user_id = await bot.fetch_user(interior_result.DISCORD_ID)
            await channel_id.set_permissions(user_id, send_messages = True)
            query = db.update(ban).where(db.and_(
                                                 ban.columns.USER_ID == banned_user_id,
                                                )
                                        )
            values = [{
                        'CURRENTLY_BANNED': 0, 
                        'UPDATE_DATE': datetime.datetime.now()
                }]
            connection.execute(query, values)

bot.run(DISCORD_TOKEN)
