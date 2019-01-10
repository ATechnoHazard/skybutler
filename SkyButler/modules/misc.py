import html, time
import json
import random
from datetime import datetime
from typing import Optional, List
import requests

from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from telegram.utils.helpers import escape_markdown, mention_html

from SkyButler import dispatcher
from SkyButler.__main__ import GDPR
from SkyButler.__main__ import STATS, USER_INFO
from SkyButler.modules.disable import DisableAbleCommandHandler
from SkyButler.modules.helper_funcs.extraction import extract_user
from SkyButler.modules.helper_funcs.filters import CustomFilters
from SkyButler.modules.translations.strings import sbt

RUN_STRINGS = (
    "Where da heck you think ya going?",
    "Run for ya life kid.. run for ya life, Chuck Norris is here.",
    "Trying to get away?",
    "Run baby run imma coming...",
    "Come on, come back ",
    "You ain't so fast kid",
    "Bangs a wall!",
    "Don't leave me alone!!",
    "You run alone, you die alone.",
    "Can't stop running eh?",
    "You're gonna regret this..",
    "Why run when you can /kickme",
    "No-one here cares.",
    "You know nothing..nothin....",
    "Run for ya life, tho it is of no value?",
    "Walkers are coming, run for ya life..",
    "Is Darth Vader around?.",
    "May the odds be ever in your favour.",
    "Famous last words before fapping",
    "Next Usian Bolt here.",
    "Have to globally blacklist this guy for running so often ",
    "Yeah yeah, just tap /kickme and get over it.",
    "Legend has it, Temple Run was based on this guy...",
    "Calma ya not so mature horses, son..",
    "How about i cut ya legs out? Evil.. AhahaAh",
    "You are running like ya wife ran away with somebody else.",
    "Run and burn ya fat.",
    "Never come back again.",
    "You can't run without a brain - get one.",
    "NO RUNNING HERE ffs",
    "Skybutler is coming to hunt you down, baby.",
    "Who let the dogs out?",
    "It's so funny, because we don't care.",
    "Ah, what a waste.",
    "Not so fast...",
    "Look out for the wall!",
    "Don't leave me alone with them!!",
    "You run, you die.",
    "Jokes on you, I'm everywhere",
    "You're gonna regret that...",
    "You could also try /kickme, I hear that's fun.",
    "Go bother someone else, no-one here cares.",
    "You can run, but you can't hide.",
    "Is that all you've got?",
    "I'm behind you...",
    "You've got company!",
    "We can do this the easy way, or the hard way.",
    "You just don't get it, do you?",
    "Yeah, you better run!",
    "Please, remind me how much I care?",
    "I'd run faster if I were you.",
    "That's definitely the droid we're looking for.",
    "May the odds be ever in your favour.",
    "Famous last words.",
    "And they disappeared forever, never to be seen again.",
    "\"Oh, look at me! I'm so cool, I can run from a bot!\" - this person",
    "Yeah yeah, just tap /kickme already.",
    "Here, take this ring and head to Mordor while you're at it.",
    "Legend has it, they're still running...",
    "Unlike Harry Potter, your parents can't protect you from me.",
    "Fear leads to anger. Anger leads to hate. Hate leads to suffering. If you keep running in fear, you might "
    "be the next Vader.",
    "Multiple calculations later, I have decided my interest in your shenanigans is exactly 0.",
    "Legend has it, they're still running.",
    "Keep it up, not sure we want you here anyway.",
    "You're a wiza- Oh. Wait. You're not Harry, keep moving.",
    "NO RUNNING IN THE HALLWAYS!",
    "Hasta la vista, baby.",
    "Who let the dogs out?",
    "It's funny, because no one cares.",
    "Ah, what a waste. I liked that one.",
    "Frankly, my dear, I don't give a damn.",
    "My milkshake brings all the boys to yard... So run faster!",
    "You can't HANDLE the truth!",
    "A long time ago, in a galaxy far far away... Someone would've cared about that. Not anymore though.",
    "Hey, look at them! They're running from the inevitable banhammer... Cute.",
    "Han shot first. So will I.",
    "What are you running after, a white rabbit?",
    "As The Doctor would say... RUN!",
    "Run Barry run",
    "Don't you want VoLTE ?",
    "Oh! Someone wants to be The Flash",
    "Nani the F***!",
    "You run, you lose.",
    "Go watch POGO!",
    "Pew Pew Pew...",
    "You think speed is your ally? I was born on treadmill.",
    "A shinigami is coming after you.",
    "I don't give a damn.",
    "Run like it's the end of the world!",
    "You can't HANDLE the truth!",
    "You can't run away from Thor's Hammer",
    "Prey is running",
    "Don't run away from me, i ain't grabbing ya, am i?",
    "KThnxBye",
    "I think you should go home or better a mental asylum.",
    "Command not found. Just like your brain.",
    "Do you realize you are making a fool of yourself? Apparently not.",
    "Bot rule 544 section 9 prevents me from replying to stupid humans like you.",
    "Sorry, we do not sell brains.",
    "Believe me you are not normal.",
    "I bet your brain feels as good as new, seeing that you never use it.",
    "If I wanted to kill myself I'd climb your ego and jump to your IQ.",
    "Zombies eat brains... you're safe.",
    "You didn't evolve from apes, they evolved from you.",
    "Come back and talk to me when your I.Q. exceeds your age.",
    "I'm not saying you're stupid, I'm just saying you've got bad luck when it comes to thinking.",
    "What language are you speaking? Cause it sounds like bullshit.",
    "Stupidity is not a crime so you are free to go.",
    "You are proof that evolution CAN go in reverse.",
    "I would ask you how old you are but I know you can't count that high.",
    "As an outsider, what do you think of the human race?",
    "Brains aren't everything. In your case they're nothing.",
    "Ordinarily people live and learn. You just live.",
    "I don't know what makes you so stupid, but it really works.",
    "Keep talking, someday you'll say something intelligent! (I doubt it though)",
    "Shock me, say something intelligent.",
    "Your IQ's lower than your shoe size.",
    "Alas! Your neurotransmitters are no more working.",
    "Everyone has the right to be stupid but you are abusing the privilege.",
    "I'm sorry I hurt your feelings when I called you stupid. I thought you already knew that.",
)

SLAP_TEMPLATES = (
    "{user1} {hits} {user2} with *{item}*. {emoji}",
    "{user1} {hits} {user2} in the face with *{item}*. {emoji}",
    "{user1} {hits} {user2} around a bit with *{item}*. {emoji}",
    "{user1} {throws} *{item}* at {user2}. {emoji}",
    "{user1} grabs *{item}* and {throws} it at {user2}'s face. {emoji}",
    "{user1} launches *{item}* in {user2}'s general direction. {emoji}",
    "{user1} starts slapping {user2} silly with *{item}*. {emoji}",
    "{user1} pins {user2} down and repeatedly {hits} them with *{item}*. {emoji}",
    "{user1} grabs up *{item}* and {hits} {user2} with it. {emoji}",
    "{user1} ties {user2} to a chair and {throws} *{item}* at them. {emoji}",
    "{user1} says HAKAI,{user2} gets destroyed. No one can escape from power of the god of destruction.",
    "{user1} blasts {user2} with a spirit bomb.",
    "{user1} throws a Kamehameha wave at {user2}.",
    "{user1} cuts {user2} into pieces using Destructo Discs.",
    "{user1} snaps his fingers causing {user2} to disintegrate from the universe.",
    "{user1} craves {user2} in the Death Note.",
)

ITEMS = (
    "a Samsung J5 2015",
    "Oreo OTA",
    "a Galaxy Grand Prime",
    "a download link",
    "a Note 4",
    "Oreo port",
    "knox 0x0",
    "prenormal RMM state",
    "unfiltered logs",
    "kanged rom",
    "VOLTE",
    "168h uptime",
    "7.1.1 port",
    "bootloops",
    "120FPS",
    "a karnel",
    "a /slap",
    "a keylogger",
    "an antikang",
    "a locked bootloader",
    "a machine gun",
    "a bugless rom",
    "stock rom",
    "audio fix",
    "a floppy disk",
    "a cup of coffee",
    "a baseball bat",
    "a printer",
    "a shovel",
    "a CRT monitor",
    "a toaster",
    "a five ton truck",
    "a roll of duct tape",
    "a book",
    "a laptop",
    "an old tv",
    "a fire extinguisher",
    "a bear",
)

THROW = (
    "throws",
    "flings",
    "chucks",
    "hurls",
)

HIT = (
    "hits",
    "whacks",
    "slaps",
    "smacks",
    "spanks",
    "bashes",
)
EMOJI = (
    "\U0001F923",
    "\U0001F602",
    "\U0001F605",
    "\U0001F606",
    "\U0001F609",
    "\U0001F60E",
    "\U0001F929",
    "\U0001F623",
)

GMAPS_LOC = "https://maps.googleapis.com/maps/api/geocode/json"
GMAPS_TIME = "https://maps.googleapis.com/maps/api/timezone/json"


SMACK_STRING = """[This is...idk...maybe...just...press...on...it](https://www.youtube.com/watch?v=VYOjWnS4cMY)"""

@run_async
def runs(bot: Bot, update: Update):
    running = update.effective_message
    if running.reply_to_message:
        update.effective_message.reply_to_message.reply_text(random.choice(RUN_STRINGS))
    else:
        update.effective_message.reply_text(random.choice(RUN_STRINGS))

@run_async
def smack(bot: Bot, update: Update):
    msg = update.effective_message
    if msg.reply_to_message:
        update.effective_message.reply_to_message.reply_text(SMACK_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)
    else:
        update.effective_message.reply_text(SMACK_STRING, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)

@run_async
def slap(bot: Bot, update: Update, args: List[str]):
    msg = update.effective_message  # type: Optional[Message]

    # reply to correct message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text

    # get user who sent message
    if msg.from_user.username:
        curr_user = "@" + escape_markdown(msg.from_user.username)
    else:
        curr_user = "[{}](tg://user?id={})".format(msg.from_user.first_name, msg.from_user.id)

    user_id = extract_user(update.effective_message, args)
    if user_id == bot.id:
        user1 = "[{}](tg://user?id={})".format(bot.first_name, bot.id)
        user2 = curr_user
    elif user_id:
        slapped_user = bot.get_chat(user_id)
        user1 = curr_user
        if slapped_user.username:
            user2 = "@" + escape_markdown(slapped_user.username)
        else:
            user2 = "[{}](tg://user?id={})".format(slapped_user.first_name,
                                                   slapped_user.id)

    # if no target found, bot targets the sender
    else:
        user1 = "[{}](tg://user?id={})".format(bot.first_name, bot.id)
        user2 = curr_user

    temp = random.choice(SLAP_TEMPLATES)
    item = random.choice(ITEMS)
    hit = random.choice(HIT)
    throw = random.choice(THROW)
    emoji = random.choice(EMOJI)

    repl = temp.format(user1=user1, user2=user2, item=item, hits=hit, throws=throw, emoji=emoji)

    reply_text(repl, parse_mode=ParseMode.MARKDOWN)


@run_async
def get_bot_ip(bot: Bot, update: Update):
    """ Sends the bot's IP address, so as to be able to ssh in if necessary.
        OWNER ONLY.
    """
    res = requests.get("http://ipinfo.io/ip")
    update.message.reply_text(res.text)


@run_async
def get_id(bot: Bot, update: Update, args: List[str]):
    user_id = extract_user(update.effective_message, args)
    if user_id:
        if update.effective_message.reply_to_message and update.effective_message.reply_to_message.forward_from:
            user1 = update.effective_message.reply_to_message.from_user
            user2 = update.effective_message.reply_to_message.forward_from
            update.effective_message.reply_text(
                "The original sender, {}, has an ID of `{}`.\nThe forwarder, {}, has an ID of `{}`.".format(
                    escape_markdown(user2.first_name),
                    user2.id,
                    escape_markdown(user1.first_name),
                    user1.id),
                parse_mode=ParseMode.MARKDOWN)
        elif update.effective_message.reply_to_message and update.effective_message.reply_to_message.forward_from_chat:
            user1 = update.effective_message.reply_to_message.from_user
            user2 = update.effective_message.reply_to_message.forward_from_chat
            update.effective_message.reply_text(
                "The channel, {}, has an ID of `{}`.\nThe forwarder, {}, has an ID of `{}`.".format(
                    escape_markdown(user2.title),
                    user2.id,
                    escape_markdown(user1.first_name),
                    user1.id),
                parse_mode=ParseMode.MARKDOWN)
        else:
            user = bot.get_chat(user_id)
            update.effective_message.reply_text(sbt(update.effective_chat.id, "{}'s id is `{}`.").format(escape_markdown(user.first_name), user.id),
                                                parse_mode=ParseMode.MARKDOWN)
    else:
        chat = update.effective_chat  # type: Optional[Chat]
        if chat.type == "private":
            update.effective_message.reply_text(sbt(update.effective_chat.id, "Your id is `{}`.").format(chat.id),
                                                parse_mode=ParseMode.MARKDOWN)

        else:
            update.effective_message.reply_text(sbt(update.effective_chat.id, "This group's id is `{}`.").format(chat.id),
                                                parse_mode=ParseMode.MARKDOWN)


@run_async
def info(bot: Bot, update: Update, args: List[str]):
    msg = update.effective_message  # type: Optional[Message]
    user_id = extract_user(update.effective_message, args)

    if user_id:
        user = bot.get_chat(user_id)

    elif not msg.reply_to_message and not args:
        user = msg.from_user

    elif not msg.reply_to_message and (not args or (
            len(args) >= 1 and not args[0].startswith("@") and not args[0].isdigit() and not msg.parse_entities(
        [MessageEntity.TEXT_MENTION]))):
        msg.reply_text(sbt(update.effective_chat.id, "I can't extract a user from this."))
        return

    else:
        return

    text = "<b>User info</b>:" \
           "\nID: <code>{}</code>" \
           "\nFirst Name: {}".format(user.id, html.escape(user.first_name))

    if user.last_name:
        text += "\nLast Name: {}".format(html.escape(user.last_name))

    if user.username:
        text += "\nUsername: @{}".format(html.escape(user.username))

    text += "\nPermanent user link: {}".format(mention_html(user.id, "link"))

    for mod in USER_INFO:
        mod_info = mod.__user_info__(user.id).strip()
        if mod_info:
            text += "\n\n" + mod_info

    update.effective_message.reply_text(text, parse_mode=ParseMode.HTML)


@run_async
def echo(bot: Bot, update: Update):
    args = update.effective_message.text.split(None, 1)
    message = update.effective_message
    if message.reply_to_message:
        message.reply_to_message.reply_text(args[1])
    else:
        message.reply_text(args[1], quote=False)
    message.delete()


@run_async
def gdpr(bot: Bot, update: Update):
    update.effective_message.reply_text("Deleting identifiable data...")
    for mod in GDPR:
        mod.__gdpr__(update.effective_user.id)

    update.effective_message.reply_text("Your personal data has been deleted.\n\nNote that this will not unban "
                                        "you from any chats, as that is telegram data, not SkyButler data. "
                                        "Flooding, warns, gbans are also preserved",
                                        parse_mode=ParseMode.MARKDOWN)

MARKDOWN_HELP = """
Markdown is a very powerful formatting tool supported by telegram. {} has some enhancements, to make sure that \
saved messages are correctly parsed, and to allow you to create buttons.

- <code>_italic_</code>: wrapping text with '_' will produce italic text
- <code>*bold*</code>: wrapping text with '*' will produce bold text
- <code>`code`</code>: wrapping text with '`' will produce monospaced text, also known as 'code'
- <code>[sometext](someURL)</code>: this will create a link - the message will just show <code>sometext</code>, \
and tapping on it will open the page at <code>someURL</code>.
EG: <code>[test](example.com)</code>

- <code>[buttontext](buttonurl:someURL)</code>: this is a special enhancement to allow users to have telegram \
buttons in their markdown. <code>buttontext</code> will be what is displayed on the button, and <code>someurl</code> \
will be the url which is opened.
EG: <code>[This is a button](buttonurl:example.com)</code>

If you want multiple buttons on the same line, use :same, as such:
<code>[one](buttonurl://example.com)
[two](buttonurl://google.com:same)</code>
This will create two buttons on a single line, instead of one button per line.

Keep in mind that your message <b>MUST</b> contain some text other than just a button!
""".format(dispatcher.bot.first_name)


@run_async
def markdown_help(bot: Bot, update: Update):
    update.effective_message.reply_text(MARKDOWN_HELP, parse_mode=ParseMode.HTML)
    update.effective_message.reply_text("Try forwarding the following message to me, and you'll see!")
    update.effective_message.reply_text("/save test This is a markdown test. _italics_, *bold*, `code`, "
                                        "[URL](example.com) [button](buttonurl:github.com) "
                                        "[button2](buttonurl://google.com:same)")


@run_async
def stats(bot: Bot, update: Update):
    update.effective_message.reply_text("Current stats:\n" + "\n".join([mod.__stats__() for mod in STATS]))


# /ip is for private use
__help__ = """
 - /id: get the current group id. If used by replying to a message, gets that user's id.
 - /runs: reply a random string from an array of replies.
 - /slap: slap a user, or get slapped if not a reply.
 - /spank: same as /slap but nastier.
 - /weather <place>: gives the weather info at the given place
 - /sudolist: gives the sudo list
 - /birthday: Try it yourself
 - /info: get information about a user.
 - /gdpr: deletes your information from the bot's database. Private chats only.

 - /markdownhelp: quick summary of how markdown works in telegram - can only be called in private chats.
"""

__mod_name__ = "Misc"

ID_HANDLER = DisableAbleCommandHandler("id", get_id, pass_args=True)
IP_HANDLER = CommandHandler("ip", get_bot_ip, filters=CustomFilters.sudo_filter)

RUNS_HANDLER = DisableAbleCommandHandler("runs", runs)
SMACK_HANDLER = DisableAbleCommandHandler("smack", smack)
SLAP_HANDLER = DisableAbleCommandHandler("slap", slap, pass_args=True)
SPANK_HANDLER = DisableAbleCommandHandler("spank", slap, pass_args=True)
INFO_HANDLER = DisableAbleCommandHandler("info", info, pass_args=True)

ECHO_HANDLER = CommandHandler("echo", echo, filters=CustomFilters.sudo_filter)
MD_HELP_HANDLER = CommandHandler("markdownhelp", markdown_help, filters=Filters.private)

STATS_HANDLER = CommandHandler("stats", stats, filters=CustomFilters.sudo_filter)
GDPR_HANDLER = CommandHandler("gdpr", gdpr, filters=Filters.private)

dispatcher.add_handler(ID_HANDLER)
dispatcher.add_handler(IP_HANDLER)
dispatcher.add_handler(RUNS_HANDLER)
dispatcher.add_handler(SMACK_HANDLER)
dispatcher.add_handler(SLAP_HANDLER)
dispatcher.add_handler(SPANK_HANDLER)
dispatcher.add_handler(INFO_HANDLER)
dispatcher.add_handler(ECHO_HANDLER)
dispatcher.add_handler(MD_HELP_HANDLER)
dispatcher.add_handler(STATS_HANDLER)
dispatcher.add_handler(GDPR_HANDLER)
