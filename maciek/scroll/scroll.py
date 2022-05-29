cp from talon import Module, actions, cron

mod = Module()
mod.tag("scroll")

scroll_direction = None
scroll_job = None
scroll_speed = 100

@mod.action_class
class Actions:
    def scroll_up():
        """Scroll up"""
    def scroll_down():
        """Scroll down"""
    def scroll_left():
        """Scroll left"""
    def scroll_right():
        """Scroll right"""
    def scroll_up_page():
        """Scroll up page"""
    def scroll_down_page():
        """Scroll down page"""
    def scroll_up_half_page():
        """Scroll up half page"""
    def scroll_down_half_page():
        """Scroll down half page"""

    def scroll_up_continuous():
        """Scroll up continuously"""
        scroll_continuous("up")

    def scroll_down_continuous():
        """Scroll down continuously"""
        scroll_continuous("down")

    def scroll_stop():
        """Stop continuous scroll"""
        global scroll_job
        if scroll_job:
            cron.cancel(scroll_job)
            scroll_job = None
            return True
        return False

    def scroll_speed_show():
        """Show scroll speed"""
        actions.user.notify("Scroll speed: {}%".format(scroll_speed))

    def scroll_speed(speed: int):
        """Set scroll speed"""
        if speed > 50:
            speed = 50
        set_scroll_speed(speed * 10)

    def scroll_speed_increase():
        """Increase scroll speed"""
        set_scroll_speed(scroll_speed + 20)

    def scroll_speed_decrease():
        """Decrease scroll speed"""
        set_scroll_speed(scroll_speed - 20)


def set_scroll_speed(speed: int):
    global scroll_speed
    scroll_speed = speed
    actions.user.scroll_speed_show()
    start_scroll_interval()

def scroll_continuous(direction: str):
    global scroll_direction
    scroll_direction = direction
    if not scroll_job:
        start_scroll_interval()

def start_scroll_interval():
    global scroll_job
    if scroll_job:
        cron.cancel(scroll_job)
    scroll_continuous_helper()
    time = round(10000 / scroll_speed)
    scroll_job = cron.interval(f"{time}ms", scroll_continuous_helper)

def scroll_continuous_helper():
    if scroll_direction == "up":
        actions.user.scroll_up()
    elif scroll_direction == "down":
        actions.user.scroll_down()
