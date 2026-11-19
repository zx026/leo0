from pyrogram import types
from pyrogram.enums import ButtonStyle

from ArtistMusic import app, config, lang

# ----------------------------------------------------------
# HELP MENU: 21 buttons (merged groups)
# (callback key, button label, [old help_* keys whose text is merged])
# ----------------------------------------------------------
HELP_GROUPS = [
    ("play",        "ᴘʟᴀʏ",           ["play"]),
    ("playback",    "ᴄᴏɴᴛʀᴏʟ",        ["pause", "resume", "skip", "stop"]),
    ("seek",        "ꜱᴇᴇᴋ/ʟᴏᴏᴘ",      ["seek", "loop", "shuffle"]),
    ("queue",       "ǫᴜᴇᴜᴇ",          ["queue", "autoplay"]),
    ("playmode",    "ᴘʟᴀʏᴍᴏᴅᴇ",       ["playmode", "link", "autoleave"]),
    ("ban",         "ʙᴀɴ/ɢ-ʙᴀɴ",      ["ban", "gban"]),              # ban text already has kick
    ("mute",        "ᴍᴜᴛᴇ/ᴍᴀꜱꜱ",      ["mute", "mass"]),
    ("promote",     "ᴀᴅᴍɪɴ/ᴀᴜᴛʜ",     ["promote", "auth"]),          # promote text already has admins
    ("group",       "ɢʀᴏᴜᴘ",          ["group", "welcome"]),         # group text already has pin
    ("clean",       "ᴄʟᴇᴀɴ",          ["purge", "zombies"]),
    ("tag",         "ᴛᴀɢ",            ["tag"]),
    ("sticker",     "ꜱᴛɪᴄᴋᴇʀ",        ["sticker"]),
    ("info",        "ɪɴꜰᴏ/ʙᴏᴛꜱ",      ["info", "bots"]),
    ("sudo",        "ꜱᴜᴅᴏ",           ["sudo"]),
    ("broadcast",   "ʙʀᴏᴀᴅᴄᴀꜱᴛ",      ["broadcast"]),
    ("blacklist",   "ʙʟᴀᴄᴋʟɪꜱᴛ",      ["blchat", "bluser"]),
    ("maintenance", "ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ",    ["maintenance"]),
    ("active",      "ᴄᴀʟʟꜱ/ʟᴏɢꜱ",     ["active", "logs"]),
    ("restart",     "ʀᴇꜱᴛᴀʀᴛ/ʟᴇᴀᴠᴇ",  ["restart", "leave"]),
    ("eval",        "ᴇᴠᴀʟ",           ["eval"]),
    ("ping",        "ᴘɪɴɢ/ꜱᴛᴀᴛꜱ",     ["ping", "stats"]),
]


class Inline:
    def __init__(self):
        self.ikm = types.InlineKeyboardMarkup
        self.ikb = types.InlineKeyboardButton

    def cancel_dl(self, text) -> types.InlineKeyboardMarkup:
        return self.ikm([[
            self.ikb(
                text=f"✗  {text}",
                callback_data="cancel_dl",
                style=ButtonStyle.DANGER,
            )
        ]])

    def controls(
        self,
        chat_id: int,
        status: str = None,
        timer: str = None,
        remove: bool = False,
    ) -> types.InlineKeyboardMarkup:
        keyboard = []

        if status:
            keyboard.append(
                [self.ikb(
                    text=f"{status}",
                    callback_data=f"controls status {chat_id}",
                    style=ButtonStyle.PRIMARY,
                )]
            )
        elif timer:
            keyboard.append(
                [self.ikb(
                    text=f"{timer}",
                    callback_data=f"controls status {chat_id}",
                    style=ButtonStyle.PRIMARY,
                )]
            )

        if not remove:
            keyboard.append(
                [
                    self.ikb(text="II",  callback_data=f"controls pause {chat_id}",  style=ButtonStyle.PRIMARY),
                    self.ikb(text="▷",   callback_data=f"controls resume {chat_id}", style=ButtonStyle.PRIMARY),
                    self.ikb(text="↻",   callback_data=f"controls replay {chat_id}", style=ButtonStyle.PRIMARY),
                    self.ikb(text="‣‣I", callback_data=f"controls skip {chat_id}",   style=ButtonStyle.PRIMARY),
                    self.ikb(text="▢",   callback_data=f"controls stop {chat_id}",   style=ButtonStyle.PRIMARY),
                ]
            )
            from ArtistMusic import db
            ap_on = chat_id in db.autoplay_on
            keyboard.append(
                [
                    self.ikb(
                        text="ᴀᴜᴛᴏᴘʟᴀʏ : ᴏɴ" if ap_on else "ᴀᴜᴛᴏᴘʟᴀʏ : ᴏғғ",
                        callback_data=f"controls autoplay {chat_id}",
                        style=ButtonStyle.SUCCESS,
                    ),
                    self.ikb(
                        text="• ᴄʟᴏsᴇ •",
                        callback_data=f"controls close {chat_id}",
                        style=ButtonStyle.DANGER,
                    ),
                ]
            )

        return self.ikm(keyboard)

    def help_markup(
        self, _lang: dict, back: bool = False
    ) -> types.InlineKeyboardMarkup:
        if back:
            rows = [
                [self.ikb(
                    text="• ʙᴀᴄᴋ •",
                    callback_data="help_main",
                    style=ButtonStyle.SUCCESS,
                )]
            ]
        else:
            _btns = [
                self.ikb(
                    text=_label,
                    callback_data=f"help_{_key}",
                    style=ButtonStyle.PRIMARY,
                )
                for _key, _label, _ in HELP_GROUPS
            ]
            rows = [_btns[n:n + 3] for n in range(0, len(_btns), 3)]
            rows.append([
                self.ikb(
                    text="• ʙᴀᴄᴋ •",
                    callback_data="start",
                    style=ButtonStyle.SUCCESS,
                )
            ])
        return self.ikm(rows)

    def help_text(self, _lang: dict, category: str):
        """Merged help text for a group key (None if category is not a group)."""
        for _key, _label, _srcs in HELP_GROUPS:
            if _key == category:
                parts = [_lang.get(f"help_{k}") for k in _srcs]
                parts = [p for p in parts if p]
                return "\n\n".join(parts) if parts else None
        return None

    def langs_markup(self) -> types.InlineKeyboardMarkup:
        langs = [
            ("🇬🇧 English",    "en"), ("🇮🇳 Hindi",      "hi"),
            ("🇮🇳 Telugu",     "te"), ("🇰🇷 Korean",     "ko"),
            ("🇲🇲 Myanmar",    "my"), ("🇮🇩 Indonesian", "id"),
            ("🇧🇷 Portuguese", "pt"), ("🇸🇦 Arabic",     "ar"),
            ("🇪🇸 Spanish",    "es"), ("🇫🇷 French",     "fr"),
            ("🇷🇺 Russian",    "ru"), ("🇩🇪 German",     "de"),
            ("🇹🇷 Turkish",    "tr"), ("🇧🇩 Bengali",    "bn"),
            ("🇹🇭 Thai",       "th"), ("🇻🇳 Vietnamese", "vi"),
            ("🇯🇵 Japanese",   "ja"), ("🇨🇳 Chinese",    "zh"),
            ("🇵🇰 Urdu",       "ur"), ("🇮🇷 Persian",    "fa"),
            ("🇮🇳 Bhojpuri",   "bho"), ("🇳🇵 Nepali",     "ne"),
        ]
        rows = []
        for i in range(0, len(langs), 2):
            row = [self.ikb(text=langs[i][0], callback_data=f"setlang_{langs[i][1]}", style=ButtonStyle.PRIMARY)]
            if i + 1 < len(langs):
                row.append(self.ikb(text=langs[i + 1][0], callback_data=f"setlang_{langs[i + 1][1]}", style=ButtonStyle.PRIMARY))
            rows.append(row)
        rows.append([self.ikb(
            text="• ʙᴀᴄᴋ •",
            callback_data="start",
            style=ButtonStyle.SUCCESS,
        )])
        return self.ikm(rows)

    # FIX #1: the 'text' param is now actually used (in the status row)
    def ping_markup(self, text: str) -> types.InlineKeyboardMarkup:
        return self.ikm([
            [
                self.ikb(
                    text=f"{text}",
                    callback_data="ping_refresh",
                    style=ButtonStyle.PRIMARY,
                ),
            ],
            [
                self.ikb(text="  ᴄʜᴀɴɴᴇʟ", url=config.SUPPORT_CHANNEL, style=ButtonStyle.PRIMARY),
                self.ikb(text="  ꜱᴜᴘᴘᴏʀᴛ",  url=config.SUPPORT_CHAT,    style=ButtonStyle.PRIMARY),
            ],
            [
                self.ikb(
                    text="ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ",
                    url=f"https://t.me/{app.username}?startgroup=true",
                    style=ButtonStyle.SUCCESS,
                ),
            ],
        ])

    # FIX #2: 'item_id' is now passed in callback_data so that the
    # correct item is controlled in a multi-track queue (the wrong item is not pressed)
    def play_queued(
        self, chat_id: int, item_id: str, _text: str
    ) -> types.InlineKeyboardMarkup:
        return self.ikm([
            [
                self.ikb(text="▷",   callback_data=f"controls resume {chat_id} {item_id}", style=ButtonStyle.PRIMARY),
                self.ikb(text="II",  callback_data=f"controls pause {chat_id} {item_id}",  style=ButtonStyle.PRIMARY),
                self.ikb(text="↻",   callback_data=f"controls replay {chat_id} {item_id}", style=ButtonStyle.PRIMARY),
                self.ikb(text="‣‣I", callback_data=f"controls skip {chat_id} {item_id}",   style=ButtonStyle.PRIMARY),
                self.ikb(text="▢",   callback_data=f"controls stop {chat_id} {item_id}",   style=ButtonStyle.PRIMARY),
            ],
        ])

    def queue_markup(
        self, chat_id: int, _text: str, playing: bool
    ) -> types.InlineKeyboardMarkup:
        _action = "pause" if playing else "resume"
        return self.ikm(
            [[self.ikb(
                text=_text,
                callback_data=f"controls {_action} {chat_id} q",
                style=ButtonStyle.SUCCESS,
            )]]
        )

    # FIX #3: 'language' is now displayed in its own row
    def settings_markup(
        self, lang: dict, admin_only: bool, force_admin: bool, language: str, chat_id: int
    ) -> types.InlineKeyboardMarkup:
        play_mode_txt  = lang["admin_only_txt"] if admin_only  else lang["everyone"]
        force_mode_txt = lang["admin_only_txt"] if force_admin else lang["everyone"]
        return self.ikm([
            [
                self.ikb(text="  " + lang["play_mode"],  callback_data=f"controls status {chat_id}", style=ButtonStyle.PRIMARY),
                self.ikb(text=play_mode_txt,               callback_data="playmode",                   style=ButtonStyle.SUCCESS),
            ],
            [
                self.ikb(text="  " + lang["force_mode"], callback_data=f"controls status {chat_id}", style=ButtonStyle.PRIMARY),
                self.ikb(text=force_mode_txt,              callback_data="forcemode",                  style=ButtonStyle.SUCCESS),
            ],
            [
                self.ikb(text="" + language.upper(),  callback_data="help_langs", style=ButtonStyle.PRIMARY),
            ],
        ])

    def start_key(
        self, lang: dict, private: bool = False
    ) -> types.InlineKeyboardMarkup:
        rows = [
            [
                self.ikb(
                    text="" + lang["add_me"],
                    url=f"https://t.me/{app.username}?startgroup=true",
                    style=ButtonStyle.PRIMARY,
                )
            ],
            [
                self.ikb(text="  " + lang["help"],  callback_data="help"),
            ],
            [
                self.ikb(text="  " + lang["support"], url=config.SUPPORT_CHAT),
                self.ikb(text=" " + lang["channel"], url=config.SUPPORT_CHANNEL),
            ],
            [
                self.ikb(text="ʟᴀɴɢᴜᴀɢᴇ",  callback_data="help_langs"),
                self.ikb(text="ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/l_Smoke_ll"),
            ],
        ]
        return self.ikm(rows)

    def yt_key(self, link: str) -> types.InlineKeyboardMarkup:
        return self.ikm([
            [
                self.ikb(text="ᴄᴏᴘʏ ʟɪɴᴋ",     copy_text=link, style=ButtonStyle.PRIMARY),
                self.ikb(text="ᴏᴘᴇɴ ɪɴ ʏᴛ", url=link,       style=ButtonStyle.DANGER),
            ],
        ])
