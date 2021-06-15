#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author   : Chiupam (https://t.me/chiupam)
# @Data     : 2021-06-15
# @Version  : v 2.5
# @Updata   :
# @Future   :


from .. import chat_id, jdbot, _ConfigDir, logger, api_id, api_hash, proxystart, proxy, _ScriptsDir, _OwnDir, _JdbotDir, TOKEN
from ..bot.utils import cmd, press_event, backfile, jdcmd, _DiyDir, V4, QL, _ConfigFile, myck
from telethon import events, TelegramClient, Button
import re, json, requests, os, asyncio


if proxystart:
    client = TelegramClient("user", api_id, api_hash, proxy=proxy, connection_retries=None).start()
else:
    client = TelegramClient("user", api_id, api_hash, connection_retries=None).start()

if not os.path.isfile(f"{_JdbotDir}/diy/bot.py"):
    os.system(f'cd {_JdbotDir}/diy/ && wget https://raw.githubusercontent.com/chiupam/JD_Diy/main/jbot/bot.py')
    if os.path.isfile(f"{_JdbotDir}/diy/bot.py"):
        os.system('pm2 restart jbot')
if not os.path.isfile(f"{_ConfigDir}/diybotset.json"):
    os.system(f'cd {_ConfigDir} && wget https://raw.githubusercontent.com/chiupam/JD_Diy/master/config/diybotset.json')


with open(f"{_ConfigDir}/diybotset.json", 'r', encoding='utf-8') as f:
    diybotset = json.load(f)
my_chat_id = int(diybotset['my_chat_id'])


bot_id = int(TOKEN.split(':')[0])


def checkCookie1():
    expired = []
    cookies = myck(_ConfigFile)
    for cookie in cookies:
        cknum = cookies.index(cookie) + 1
        if checkCookie2(cookie):
            expired.append(cknum)
    return expired, cookies


def checkCookie2(cookie):
    url = "https://me-api.jd.com/user_new/info/GetJDUserInfoUnion"
    headers = {
        "Host": "me-api.jd.com",
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Cookie": cookie,
        "User-Agent": "jdapp;iPhone;9.4.4;14.3;network/4g;Mozilla/5.0 (iPhone; CPU iPhone OS 14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1",
        "Accept-Language": "zh-cn",
        "Referer": "https://home.m.jd.com/myJd/newhome.action?sceneval=2&ufc=&",
        "Accept-Encoding": "gzip, deflate, br"
    }
    try:
        r = requests.get(url, headers=headers).json()
        if r['retcode'] == '1001':
            return True
        else:
            return False
    except:
        return False


def getbean(i, cookie, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "Cookie": cookie,
    }
    result, o = '', '\n\t\t└'
    try:
        r = requests.get(url=url, headers=headers)
        res = r.json()

        if res['code'] == '0':
            followDesc = res['result']['followDesc']
            if followDesc.find('成功') != -1:
                try:
                    for n in range(len(res['result']['alreadyReceivedGifts'])):
                        redWord = res['result']['alreadyReceivedGifts'][n]['redWord']
                        rearWord = res['result']['alreadyReceivedGifts'][n]['rearWord']
                        result += f"{o}领取成功，获得{redWord}{rearWord}"
                except:
                    giftsToast = res['result']['giftsToast'].split(' \n ')[1]
                    result = f"{o}{giftsToast}"
            elif followDesc.find('已经') != -1:
                result = f"{o}{followDesc}"
        else:
            result = f"{o}Cookie 可能已经过期"
    except Exception as e:
        if str(e).find('(char 0)') != -1:
            result = f"{o}访问发生错误：无法解析数据包"
        else:
            result = f"{o}访问发生错误：{e}"
    return f"\n京东账号{i}{result}\n"


# user?
@client.on(events.NewMessage(chats=[bot_id, my_chat_id], from_users=chat_id, pattern=r"^user(\?|\？)$"))
async def fortest(event):
    try:
        msg = await jdbot.send_message(chat_id, '你好无聊。。。\n我在监控。。。\n不要烦我。。。')
        await asyncio.sleep(5)
        await jdbot.delete_messages(chat_id, msg)
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


@client.on(events.NewMessage(chats=[-1001197524983, my_chat_id], pattern=r'.*店'))
async def shopbean(event):
    cookies = myck(_ConfigFile)
    message = event.message.text
    url = re.findall(re.compile(r"[(](https://api\.m\.jd\.com.*?)[)]", re.S), message)
    if url != [] and len(cookies) > 0:
        i = 0
        info = '关注店铺\n' + message.split("\n")[0] + "\n"
        for cookie in cookies:
            try:
                i += 1
                info += getbean(i, cookie, url[0])
            except:
                continue
        await jdbot.send_message(chat_id, info)


# @client.on(events.NewMessage(chats=[-1001169232926, my_chat_id], pattern=r"^export\s"))
# async def myexport(event):
#     """
#     监控组队瓜分ID
#     关注频道：https://t.me/zuduifendou
#     """
#     try:
#         messages = event.message.text.split("\n")
#         start = await jdbot.send_message(chat_id, "监控到新的 activityId，准备自动替换")
#         for message in messages:
#             kv = message.replace("export ", "").replace("*", "")
#             kname = kv.split("=")[0]
#             vname = re.findall(r"(\".*\"|'.*')", kv)[0][1:-1]
#             with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f1:
#                 configs = f1.read()
#             if configs.find(kname) != -1:
#                 configs = re.sub(f'{kname}=(\"|\').*(\"|\')', kv, configs)
#                 end = "替换环境变量成功"
#             else:
#                 if V4:
#                     with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f2:
#                         configs = f2.readlines()
#                     for config in configs:
#                         if config.find("第五区域") != -1 and config.find("↑") != -1:
#                             end_line = configs.index(config)
#                             break
#                     configs.insert(end_line - 2, f'export {kname}="{vname}"\n')
#                     configs = ''.join(configs)
#                 else:
#                     with open(f"{_ConfigDir}/config.sh", 'r', encoding='utf-8') as f2:
#                         configs = f2.read()
#                     configs += f'export {kname}="{vname}"\n'
#                 end = "新增环境变量成功"
#             with open(f"{_ConfigDir}/config.sh", 'w', encoding='utf-8') as f3:
#                 f3.write(configs)
#         await asyncio.sleep(1.5)
#         await jdbot.delete_messages(chat_id, start)
#         await jdbot.send_message(chat_id, end)
#     except Exception as e:
#         await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
#         logger.error('something wrong,I\'m sorry\n' + str(e))


@client.on(events.NewMessage(chats=[-1001419355450, my_chat_id], pattern=r"^#开卡"))
async def myzoo(event):
    """
    动物园开卡
    关注频道：https://t.me/zoo_channel
    """
    try:
        messages = event.message.text
        url = re.findall(re.compile(r"[(](https://raw\.githubusercontent\.com.*?)[)]", re.S), messages)
        if url == []:
            return
        else:
            url = url[0]
        speeds = ["http://ghproxy.com/", "https://mirror.ghproxy.com/", ""]
        for speed in speeds:
            resp = requests.get(f"{speed}{url}").text
            if resp:
                break
        if resp:
            fname = url.split('/')[-1]
            fname_cn = re.findall(r"(?<=new\sEnv\(').*(?=')", resp, re.M)
            if fname_cn != []:
                fname_cn = fname_cn[0]
            else:
                fname_cn = ''
            fpath = f"{_OwnDir}/{fname}"
            backfile(fpath)
            with open(fpath, 'w+', encoding='utf-8') as f:
                f.write(resp)
            cmdtext = False
            async with jdbot.conversation(int(chat_id), timeout=60) as conv:
                btns = [Button.inline("是", data="confirm"), Button.inline("否", data="no"), Button.inline("取消对话", data="cancel")]
                msg = await jdbot.send_message(chat_id, f"是否运行{fname_cn}开卡脚本", buttons=btns)
                convdata = await conv.wait_event(press_event(int(chat_id)))
                res = bytes.decode(convdata.data)
                if res == "cancel":
                    await jdbot.edit_message(msg, '对话已取消，感谢你的使用')
                    conv.cancel()
                    return
                elif res == "no":
                    await jdbot.edit_message(msg, f"{fname_cn}脚本将保存到{_ScriptsDir}目录")
                else:
                    cmdtext = f'{jdcmd} {fpath} now'
                    await jdbot.edit_message(msg, f"{fname_cn}脚本将保存到{_ScriptsDir}目录，且将运行它")
                conv.cancel()
            if cmdtext:
                await cmd(cmdtext)
    except exceptions.TimeoutError:
        msg = await jdbot.edit_message(msg, f'选择已超时，对话已停止\n后续如需执行，请发送\n```/cmd {jdcmd} {fpath} now```')
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


@client.on(events.NewMessage(chats=[-1001431256850, my_chat_id]))
async def myupuser(event):
    """
    关注频道：https://t.me/jd_diy_bot_channel
    """
    try:
        if event.message.file:
            fname = event.message.file.name
            try:
                if fname.endswith("bot.py") or fname.endswith("user.py"):
                    path = f'{_JdbotDir}/diy/{fname}'
                    backfile(path)
                    await client.download_file(input_location=event.message, file=path)
                    await restart()
            except:
                return
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


async def restart():
    try:
        if V4:
            await jdbot.send_message(chat_id, "v4用户，准备重启机器人")
            os.system("pm2 restart jbot")
        elif QL:
            await jdbot.send_message(chat_id, "青龙用户，准备重启机器人")
            os.system("ql bot")
        else:
            await jdbot.send_message(chat_id, "未知用户，自行重启机器人")
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))


async def upuser(fname, msg):
    try:
        furl_startswith = "https://raw.githubusercontent.com/chiupam/JD_Diy/master/jbot/"
        speeds = ["http://ghproxy.com/", "https://mirror.ghproxy.com/", ""]
        msg = await jdbot.edit_message(msg, "开始下载文件")
        for speed in speeds:
            resp = requests.get(f"{speed}{furl_startswith}{fname}").text
            if "#!/usr/bin/env python3" in resp:
                break
        if resp:
            msg = await jdbot.edit_message(msg, f"下载{fname}成功")
            path = f"{_JdbotDir}/diy/user.py"
            backfile(path)
            with open(path, 'w+', encoding='utf-8') as f:
                f.write(resp)
            await restart()
        else:
            await jdbot.edit_message(msg, f"下载{fname}失败，请自行拉取文件进/jbot/diy目录")
    except Exception as e:
        await jdbot.send_message(chat_id, 'something wrong,I\'m sorry\n' + str(e))
        logger.error('something wrong,I\'m sorry\n' + str(e))