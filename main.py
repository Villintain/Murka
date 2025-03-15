print("Start")
#ИМПОРТ (озамещение)
import random
import json
import disnake  # type: ignore
from disnake.ext import commands    # type: ignore
import sqlite3 as sq

import colorama # type: ignore
from colorama import init   # type: ignore
from colorama import Fore, Back, Style # type: ignore
init()

command_sync_flags = commands.CommandSyncFlags.default()
command_sync_flags.sync_commands_debug = False



# class Role():
#     def __init__(self):
#         self.name = None
#         self.color = None

#     def create(self,name,color):
#         self.name = name
#         self.color = color




# companyname = 'Паденеи'
# RoleMaster = Role()
# RoleMaster.create(f"Мастер {companyname}", 0xFFFFF)

# print(RoleMaster.name, RoleMaster.color)








print("Connect Config")
#СЕКРЕТНАЯ ИНФОРМАЦИЯ
with open('config.json', 'r') as file:
    config = json.load(file)

print("bot=bot")
#Определение
bot = commands.Bot(
    command_prefix=config['PREFIX'],
    intents=disnake.Intents.all(),
    command_sync_flags=command_sync_flags,
    test_guilds=[config['TEST_SERVER']],
    activity=disnake.Game(name="DnD")
    )



#КОД
#StartUP
@bot.event 
async def on_ready():

    conn = sq.connect('DND.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS Company (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   guildid INTEGER NOT NULL,
                   name TEXT NOT NULL,
                   master TEXT NOT NULL,
                   player TEXT
                   )""")
    conn.commit()
    conn.close()


    print(Fore.GREEN+f'{bot.user.name} ready!')
    print("###  # #")
    print("# #  ##")
    print("###  # #"+Fore.WHITE)




@bot.slash_command(name="createcompany",description="Создаёт новую компанию")
async def createcompany(ctx,name_comp:str,master_c:disnake.Member,player:disnake.Member):
    guild = ctx.guild


    #Создание ролей 
    await ctx.guild.create_role(name=f"Мастер {name_comp}", color=0xC71585)
    await ctx.guild.create_role(name=f"Игрок {name_comp}", color=0x349864)
    roleCompMaster = disnake.utils.get(ctx.guild.roles,name=f'Мастер {name_comp}')
    roleCompPlayer = disnake.utils.get(ctx.guild.roles,name=f'Игрок {name_comp}')
    roleMaster = disnake.utils.get(ctx.guild.roles, id = 1350095630575468619)
    rolePl = disnake.utils.get(ctx.guild.roles, id = 1350095445321453658)
    


    #Выдача ролей
    await master_c.add_roles(roleMaster)
    await player.add_roles(rolePl)
    await master_c.add_roles(roleCompMaster)
    await player.add_roles(roleCompPlayer)
    # await guild.create_category(name="Общие")




    #Создание каналов 
    categary_comp = await ctx.guild.create_category(name=name_comp)
    await categary_comp.set_permissions(ctx.guild.default_role, read_messages=False)
    await categary_comp.set_permissions(roleCompMaster, read_messages=True)
    

    dm_chanel = await guild.create_text_channel(name="ДМ-ская",category=categary_comp)
    await dm_chanel.set_permissions(ctx.guild.default_role, read_messages=False)
    await dm_chanel.set_permissions(roleCompMaster, read_messages=True)


    chat_chanel = await guild.create_text_channel(name="Чат",category=categary_comp)
    await chat_chanel.set_permissions(ctx.guild.default_role, read_messages=False)
    await chat_chanel.set_permissions(roleCompPlayer, read_messages=True)
    await chat_chanel.set_permissions(roleCompMaster, read_messages=True)

    voice_chanel = await guild.create_voice_channel(name="Игра",category=categary_comp)
    await voice_chanel.set_permissions(ctx.guild.default_role, read_messages=False)
    await voice_chanel.set_permissions(roleCompPlayer, read_messages=True)
    await voice_chanel.set_permissions(roleCompMaster, read_messages=True,move_members=True)


    private_chanel = await guild.create_voice_channel(name="Приват",category=categary_comp,user_limit=2)
    await private_chanel.set_permissions(ctx.guild.default_role, read_messages=False)
    await private_chanel.set_permissions(roleCompMaster, read_messages=True,move_members=True)



    #SQL Забота
    conn = sq.connect('DND.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Company (guildid,name,master,player) VALUES (?, ?, ?, ?)',(int(guild.id),name_comp,str(master_c),str(player)))
    conn.commit()
    conn.close()



    
if __name__ == '__main__':
    print("Bot Start")
    bot.run(config['TOKEN'])
else:
    raise SystemExit("ITS NOT LIB")










# @bot.slash_command(name="startup",description="Создать роли для работы")
# async def start(ctx):
#     guild = ctx.guild
#     await ctx.send("Ок?")
#     await guild.create_role(name="-Модератор-", color=0x6A5ACD,hoist=True,permissions=disnake.Permissions(
#         priority_speaker=True,
#         send_messages=True,
#         read_messages=True,
#         create_events=True
#         ))
#     await guild.create_role(name="---Мастер---", color=0xC71585,hoist=True,permissions=disnake.Permissions(
#         priority_speaker=True,
#         send_messages=True,
#         read_messages=True,
#         create_events=True
#         ))
#     await guild.create_role(name="---Игрок---", color=0x349864,hoist=True,permissions=disnake.Permissions(
#         send_messages=True,
#         read_messages=True
#         ))
    
#     category_obsh = guild.create_category(name="Общие")
    
#     await guild.create_text_channel(name="Модерская",category=category_obsh)
#     await guild.create_text_channel(name="Матеровая",category=category_obsh)
#     await guild.create_text_channel(name="Чат",category=category_obsh)

