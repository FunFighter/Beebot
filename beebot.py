import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import time
import requests as rq
from keys import *
import os
import libtmux as l
import mods

#@TODO make job that makes the Tmux server start or build the MCProcess before hand
# Use mutliload to start the server hosting stuff to take care of the problem above

client = commands.Bot(command_prefix = '//')
s = l.Server()
open_sessions = str(s.list_sessions())
#Check to see if session is started or not started.

if ("MC" not in open_sessions):
    print('The session does not exist, creating session')
    session = s.new_session('MC')
    window = session.new_window(attach=True, window_name="MCProcess")
    pane = window.select_pane("MCProcess")
else:
    print('The session exist, attaching to session')
    #s.attach_session('MC')
    session = s.find_where({ "session_name": "MC" })
    window = session.attached_window
    pane = window.select_pane("MCProcess")

#@TODO add to a mods folder
def returnInsult():
    res = rq.get("https://evilinsult.com/generate_insult.php?lang=en&type=text")
    res = res.content.decode('utf-8')
    return res

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error
 
@client.event
async def on_ready():
    print('BeeBot Initiated')
    try:
        print("StartSeverHit")
        pane.send_keys('cd /Users/brandonleal/OneDrive/MCServer/MC')
        pane.send_keys('sh /Users/brandonleal/OneDrive/MCServer/MC/ServerStart.sh')
    except:
        print("IT FAILED UWU!!!!")

#does pass context even need to be there???
@client.command(pass_context = True)
async def sc(ctx,*,msg):
    ''' Sends command to the tmux session from the discord channel named beebot takes in message
    '''
    # Check if its in the right channel 
    if ctx.channel.name == 'beehive':
        msg = msg.lower()
        if (msg == 'stop' or 'op' in msg):
            await ctx.send(returnInsult())
            pass
        else:
            try:
                pane.send_keys(f'{msg}',enter=True,suppress_history=False)
                # return the output of the terminal
                time.sleep(1)
                outputCon = f'\n'.join(pane.cmd('capture-pane', '-p').stdout)
                outputCon = str(outputCon)
                cleanList = outputCon.split('\n')[-3:]
                linedList = "\n".join(cleanList)
                await ctx.send(linedList)
            except Exception as e:
                print("IT FAILED UWU!!!!\n "+e)
                await ctx.send(f'{ctx} is what im getting \n Hi you used this command :)')
    else:
        await ctx.send(returnInsult())

#does pass context even need to be there???
@client.command(pass_context = True)
async def tp(ctx,*,msg):
    ''' 
        Sends "tp" then the string returned from msg to the server terminal.
    '''
    # Check if its in the right channel 
    if ctx.channel.name == 'tp':
        msg = msg.lower()
        try:
            pane.send_keys(f'tp {msg}',enter=True,suppress_history=False)
            # return the output of the terminal
            time.sleep(1)
            outputCon = f'\n'.join(pane.cmd('capture-pane', '-p').stdout)
            outputCon = str(outputCon)
            cleanList = outputCon.split('\n')[-3:]
            linedList = "\n".join(cleanList)
            await ctx.send(linedList)
        except Exception as e:
            print("IT FAILED TO TELEPORT UWU!!!!\n "+e)
            await ctx.send(f'{ctx} \n')
    else:
        await ctx.send(returnInsult())


client.run(APITOKEN)
