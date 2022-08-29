from talon import ctrl, ui, Module, Context, actions, clip, app, noise, cron
from user.knausj_talon.games.screen_regions import tap, hold, short_hold, get_from_regions, show_overlay, hide_overlay

overlay = False
current_keys = None
cron_job = None
holding = set()

region_functions = [
    [ tap("left"),     short_hold("m"),  tap("up")       ],
    [ short_hold("j"), tap("a"),         short_hold("k") ],
    [ tap("down"),     short_hold("n"),  tap("right")    ]
]
walk_region_keys = [
    [ ["s","f"], ["f"], ["f","g"]  ],
    [ ["s"],     [],    ["g"]      ],
    [ ["s","d"], ["d"], ["g","d"] ]
]
run_region_keys = [
    [ ["j","m"], ["m"], ["m","k"]  ],
    [ ["j"],     [],    ["k"]      ],
    [ ["j","n"], ["n"], ["n","k"] ]
]
look_region_keys = [
    [ ["o","u"], ["o"], ["o","i"]  ],
    [ ["u"],     [],    ["i"]      ],
    [ ["u","p"], ["p"], ["i","p"] ]
]

def make_job(region_keys):
    def job():
        global holding
        new_holding = set()
        keys = get_from_regions(region_keys)
        for k in keys:
            new_holding.add(k)
        stop_holding = holding.difference(new_holding)
        for k in stop_holding:
            actions.key(k+":up")
        holding = new_holding
        for k in holding:
            actions.key(k+":down")
    return job

def release_all():
    global holding
    for k in ["j","k","n","m","u","i","o","p","s","d","f","g"]:
        actions.key(k+":up")
    holding = set()

def stop_cron_job():
    global cron_job
    global current_keys
    if cron_job:
        cron.cancel(cron_job)
        release_all()
        cron_job = None
        current_keys = None
        hide_overlay()

def start_cron_job(region_keys):
    global cron_job
    global current_keys
    stop_cron_job()
    job = make_job(region_keys)
    cron_job = cron.interval("60ms", job)
    current_keys = region_keys
#    if overlay:
    show_overlay(region_keys)

mod = Module()
@mod.action_class
class Actions:
    def ns_walk(): 
        """Nintendo switch walk action overrideable by contexts"""
        print("ns walk action")
    
    def ns_run(): 
        """Nintendo switch run action overrideable by contexts"""
        print("ns run action")
    
    def ns_look(): 
        """Nintendo switch look action overrideable by contexts"""
        print("ns look action")
    
    def ns_toggle_overlay(): 
        """Nintendo switch toggle overlay action overrideable by contexts"""
        print("ns toggle overlay action")
    
    def ns_hide_overlay(): 
        """Nintendo switch hide overlay action overrideable by contexts"""
        print("ns hide overlay action")
    
    def ns_empty_overlay(): 
        """Nintendo switch show empty overlay action overrideable by contexts"""
        print("ns show empty overlay action")

ctx = Context()
ctx.matches = r"""
os: windows
app.name: OBS Studio
"""
@ctx.action_class("user")
class nintendo_switch_user:
    def pop():
        global cron_job
        if cron_job:
            stop_cron_job()
        else:
            get_from_regions(region_functions)()

    def ns_walk():
        start_cron_job(walk_region_keys)

    def ns_run():
        start_cron_job(run_region_keys)

    def ns_look():
        start_cron_job(look_region_keys)

    def ns_toggle_overlay():
        global overlay
        overlay = not overlay

    def ns_hide_overlay():
        hide_overlay()

    def ns_empty_overlay():
        show_overlay([
            [[],[],[]],
            [[],[],[]],
            [[],[],[]]
        ])
