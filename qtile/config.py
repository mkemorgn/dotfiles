
from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.command import lazy
from scripts import ShellScript
import os
import subprocess
import re

mod = "mod4"                                        #sets mod key
terminal = "alacritty"                              #your terminal
myConfig = "/home/mike/.config/qtile/config.py"     #config file location
qtile_log = ".local/share/qtile/qtile.log"
browser = "brave"                                   #default browser

####################################################################################################

# Hooks

#restart and reload config when screens are changed
@hook.subscribe.screen_change
def restart_on_randr(qtile):
    qtile.cmd_restart()

#@hook.subscribe.startup_once
# def autostart():
#    home = os.path.expanduser('~/styli.sh/styli.sh')
#    subprocess.call([home])

####################################################################################################

# Key Bindings

keys = [

    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Switch focus to specific monitor (out of three)
    Key([mod, "shift"], "w",lazy.to_screen(0),desc='Keyboard focus to monitor 1'),
    Key([mod, "shift"], "e",lazy.to_screen(1),desc='Keyboard focus to monitor 2'),
    Key([mod, "shift"], "r",lazy.to_screen(2),desc='Keyboard focus to monitor 3'),
    
    # Switch focus of monitors
    Key([mod], "period", lazy.next_screen(), desc="Move focus to next monitor"),
    Key([mod], "comma", lazy.prev_screen(), desc="Move focus to previous monitor"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod, "shift"], "c", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    #Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # apps
    Key([mod], "z", lazy.spawn("pcmanfm"), desc="Launch pcmanfm"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Rofi Launcher"),
    Key([mod], "b", lazy.spawn(browser), desc="Launch browser"),
    Key([mod], "m", lazy.spawn("spotify"), desc="Launch spotify"),
    Key([mod], "c", lazy.spawn("code"), desc="Launch VSCode"),
    Key([mod], "s", lazy.spawn("slack"), desc="Launch slack"),
    Key([mod], "e", lazy.spawn("emacsclient -c -a emacs"), desc="Launch emacs"),
    Key([mod], "p", lazy.spawn("postman"), desc="Launch postman"),

    # Maintenance
    Key([mod, "control"], "1", lazy.spawn(terminal+" -e vim .local/share/qtile/qtile.log"), desc="Launch qtile log"),
    Key([mod, "control"], "2", lazy.spawn(terminal+" -e vim .config/qtile/config.py"), desc="Launch qtile config"),
    
    # Sound
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer set 'Master' 10%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer set 'Master' 10%+")),
    Key([], "XF86AudioPlay", lazy.spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify " "/org/mpris/MediaPlayer2 " "org.mpris.MediaPlayer2.Player.PlayPause")),
    Key([], "XF86AudioNext", lazy.spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify " "/org/mpris/MediaPlayer2 " "org.mpris.MediaPlayer2.Player.Next")),
    Key([], "XF86AudioPrev", lazy.spawn("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify " "/org/mpris/MediaPlayer2 " "org.mpris.MediaPlayer2.Player.Previous")),
   ]

####################################################################################################

# Mouse config
# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]
####################################################################################################

# Groups

group_names = [("WWW", {'layout': 'monadtall'}),
               ("DEV", {'layout': 'monadtall'}),
               ("DOC", {'layout': 'monadtall'}),
               ("MUS", {'layout': 'monadtall'}),
               ("CHAT", {'layout': 'monadtall'}),
               ("SYS", {'layout': 'monadtall'}),
               ("PHOTO", {'layout': 'floating'})]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group

####################################################################################################

# Layouts

layout_theme = {"border_width": 2,
                "margin": 6,
                "border_focus": "#b8bb26",
                "border_normal": "#2C323B"
                }

layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Tile(shift_windows=True, **layout_theme),
    layout.Stack(num_stacks=2),
    layout.Floating(**layout_theme)
]

# Color codes from gruvbox
COLS = {
    "dark_0": "#1d2021",
    "dark_1": "#282828",
    "dark_2": "#32302f",
    "dark_3": "#3c3836",
    "dark_4": "#504945",
    "dark_5": "#665c54",
    "dark_6": "#7c6f64",
    "gray_0": "#928374",
    "light_0": "#f9f5d7",
    "light_1": "#fbf1c7",
    "light_2": "#f2e5bc",
    "light_3": "#ebdbb2",
    "light_4": "#d5c4a1",
    "light_5": "#bdae93",
    "light_6": "#a89984",
    "red_0": "#fb4934",
    "red_1": "#cc241d",
    "red_2": "#9d0006",
    "green_0": "#b8bb26",
    "green_1": "#98971a",
    "green_2": "#79740e",
    "yellow_0": "#fabd2f",
    "yellow_1": "#d79921",
    "yellow_2": "#b57614",
    "blue_0": "#83a598",
    "blue_1": "#458588",
    "blue_2": "#076678",
    "purple_0": "#d3869b",
    "purple_1": "#b16286",
    "purple_2": "#8f3f71",
    "aqua_0": "#8ec07c",
    "aqua_1": "#689d6a",
    "aqua_2": "#427b58",
    "orange_0": "#fe8019",
    "orange_1": "#d65d0e",
    "orange_2": "#af3a03",
    # Additional related colors from the deus colorscheme
    'deus_1': '#2C323B',
    'deus_2': '#646D7A',
    'deus_3': '#48505D',
    'deus_4': '#1A222F',
    'deus_5': '#101A28',
}

FONT = 'TerminessTTF Nerd Font Medium'
FOREGROUND = COLS['light_3']
ALERT = COLS['red_1']
FONTSIZE = 15
PADDING = 3

FONT_PARAMS = {
    'font': FONT,
    'fontsize': FONTSIZE,
    'foreground': FOREGROUND,
}

####################################################################################################

# Default widget settings

widget_defaults = dict(
    font="Ubuntu Mono",
    fontsize = 12,
    padding = 2,
    background=COLS["dark_1"]
)
extension_defaults = widget_defaults.copy()

####################################################################################################

# Mouse Callbacks

def update_arch():
    qtile.cmd_spawn(terminal + ' -e sudo pacman -Syu')

def wifi_list():
    qtile.cmd_spawn('nm-applet')

def bluetooth_list():
    qtile.cmd_spawn('blueman-applet')

####################################################################################################

# Screen(s)
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(
                    font="Arial", foreground=COLS["dark_4"],
                    # font="Arial", foreground=COLS["deus_3"],
                    text="◢", fontsize=50, padding= -1
                ),
                widget.GroupBox(
                    borderwidth = 8,
                    margin_y = 5,
                    margin_x = 0,
                    padding_y = 7,
                    padding_x = 4,
                    center_aligned = True,
                    active = COLS["light_2"],
                    inactive = COLS["dark_2"],
                    rounded = False,
                    highlight_color = COLS["blue_1"],
                    urgent_border = COLS["red_1"],
                    highlight_method = "line",
                    this_current_screen_border = COLS["blue_1"],
                    this_screen_border = COLS["blue_0"],
                    other_current_screen_border = COLS["orange_0"],
                    other_screen_border = COLS["orange_0"],
                    background = COLS["dark_4"],
                    fontsize = 12,
                    font=FONT
                ),
                widget.TextBox(
                    font="Arial", foreground=COLS["dark_4"],
                    # font="Arial", foreground=COLS["deus_3"],
                    text="◤ ", fontsize=50, padding=-5
                ),
                widget.WindowName(
                    padding = 0,
                    **FONT_PARAMS,
                ),

                #RIGHT SIDE
                #widget.Prompt(), #qtile spawn
                widget.Sep(
                    linewidth = 0,
                    padding = 400,
                    #foreground = colors[2],
                    #background = colors[0]
                ),
                widget.Mpris2(
                    name='spotify',
                    objname='org.mpris.MediaPlayer2.spotify',
                    display_metadata=['xesam:title', 'xesam:artist'],
                    scroll_chars=None,
                    stop_pause_text='',
                    **FONT_PARAMS,
                ),
                widget.Spacer(length = 10),
                widget.CPUGraph(
                    border_color=COLS["yellow_1"],
                    graph_color=COLS["yellow_1"],
                    border_width=1,
                    line_width=1,
                    type="line",
                    width=50,  
                    **FONT_PARAMS,
                ), 
                widget.Spacer(length = 5),
                widget.MemoryGraph(
                    border_color=COLS["blue_2"],
                    graph_color=COLS["blue_2"],
                    border_width=1,
                    line_width=1,
                    type="line",
                    width=50,
                    **FONT_PARAMS,
                ), 
                widget.Spacer(length = 5),
                widget.NetGraph(
                    border_color=COLS["green_1"],
                    graph_color=COLS["green_1"],
                    border_width=1,
                    line_width=1,
                    type="line",
                    width=50,
                    **FONT_PARAMS,
                ), 
                widget.Spacer(length = 5),
                widget.Wlan(
                    disconnected_message= 'Wifi Off',
                    format = '{essid} | Strength:{percent:2.0%}',
                    interface = 'wlan0',
                    update_interval = 10,
                    mouse_callbacks = {'Button1': wifi_list},
                    **FONT_PARAMS,
                ),
                #battery widget
                ShellScript(
                    fname = "battery.sh",
                    update_interval = 60,
                    markup = True,
                    padding = 1,
                    **FONT_PARAMS,
                ),
                widget.CheckUpdates(
                    distro = 'Arch',
                    display_format = 'Updates: {updates}',
                    no_update_string = 'Updates: N/A',
                    update_interval = 1800,
                    colour_have_updates = COLS["green_0"],
                    mouse_callbacks = {'Button1': update_arch},
                    **FONT_PARAMS,
                ),
                widget.Clock(
                    format=' %m-%d-%Y %a %H:%M',
                    **FONT_PARAMS,
                ),
                widget.Systray(),
                widget.Spacer(length = 10)
            ],
            24,
        ),
    ),
Screen(
    top=bar.Bar(
        [
            widget.TextBox(
                font="Arial", foreground=COLS["dark_4"],
                # font="Arial", foreground=COLS["deus_3"],
                text="◢", fontsize=50, padding= -1
            ),
            widget.GroupBox(
                borderwidth = 8,
                margin_y = 5,
                margin_x = 0,
                padding_y = 7,
                padding_x = 4,
                center_aligned = True,
                active = COLS["light_2"],
                inactive = COLS["dark_2"],
                rounded = False,
                highlight_color = COLS["blue_1"],
                urgent_border = COLS["red_1"],
                highlight_method = "line",
                this_current_screen_border = COLS["blue_1"],
                this_screen_border = COLS["blue_0"],
                other_current_screen_border = COLS["orange_0"],
                other_screen_border = COLS["orange_0"],
                background = COLS["dark_4"],
                fontsize = 12,
                font=FONT
            ),
            widget.TextBox(
                font="Arial", foreground=COLS["dark_4"],
                # font="Arial", foreground=COLS["deus_3"],
                text="◤ ", fontsize=50, padding=-5
            ),
            widget.WindowName(
                padding = 0,
                **FONT_PARAMS,
            ),

            #RIGHT SIDE
            #widget.Prompt(), #qtile spawn
            widget.Sep(
                linewidth = 0,
                padding = 400,
                #foreground = colors[2],
                #background = colors[0]
            ),
            widget.Mpris2(
                name='spotify',
                objname='org.mpris.MediaPlayer2.spotify',
                display_metadata=['xesam:title', 'xesam:artist'],
                scroll_chars=None,
                stop_pause_text='',
                **FONT_PARAMS,
            ),
            widget.Spacer(length = 10),
            widget.CPUGraph(
                border_color=COLS["yellow_1"],
                graph_color=COLS["yellow_1"],
                border_width=1,
                line_width=1,
                type="line",
                width=50,  
                **FONT_PARAMS,
            ), 
            widget.Spacer(length = 5),
            widget.MemoryGraph(
                border_color=COLS["blue_2"],
                graph_color=COLS["blue_2"],
                border_width=1,
                line_width=1,
                type="line",
                width=50,
                **FONT_PARAMS,
            ), 
            widget.Spacer(length = 5),
            widget.NetGraph(
                border_color=COLS["green_1"],
                graph_color=COLS["green_1"],
                border_width=1,
                line_width=1,
                type="line",
                width=50,
                **FONT_PARAMS,
            ), 
            widget.Spacer(length = 5),
            widget.Wlan(
                disconnected_message= 'Wifi Off',
                format = '{essid} | Strength:{percent:2.0%}',
                interface = 'wlan0',
                update_interval = 10,
                mouse_callbacks = {'Button1': wifi_list},
                **FONT_PARAMS,
            ),
            #battery widget
            ShellScript(
                fname = "battery.sh",
                update_interval = 60,
                markup = True,
                padding = 1,
                **FONT_PARAMS,
            ),
            widget.CheckUpdates(
                distro = 'Arch_checkupdates',
                display_format = 'Updates: {updates}',
                no_update_string = 'Updates: N/A',
                update_interval = 1800,
                colour_have_updates = COLS["green_0"],
                mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + '-e sudo pacman -Syu')},
                **FONT_PARAMS,
            ),
            widget.Clock(
                format=' %m-%d-%Y %a %H:%M',
                **FONT_PARAMS,
            ),
            widget.Systray(),
            widget.Spacer(length = 10)
        ],
        24,
        ),
    ),
]
####################################################################################################

# Everything else

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    Match(wm_type='utility'),
    Match(wm_type='notification'),
    Match(wm_type='toolbar'),
    Match(wm_type='splash'),
    Match(wm_type='dialog'),
    Match(wm_class='file_progress'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/styli.sh/styli.sh')
    subprocess.call([home])

