from typing import Tuple

from talon import Context, Module, canvas, cron, ctrl, cron

class MouseGuide:
    def __init__(self, width: float, height: float):
        self.enabled = False
        self.canvas = None
        self.job = None
        self.last_pos = None
        self.width = width
        self.height = height

    def enable(self):
        if self.enabled:
            return
        self.enabled = True
        self.last_pos = None
        self.canvas = canvas.Canvas(0, 0, self.width + 2, self.height + 2)
        self.check_mouse()
        self.canvas.register('mousemove', self.on_mouse)
        self.canvas.register('draw', self.draw_canvas)
        self.canvas.freeze()
        # uncomment this if the mouse movement event isn't working
        self.job = cron.interval('16ms', self.check_mouse)

    def disable(self):
        if not self.enabled:
            return
        cron.cancel(self.job)
        self.enabled = False
        self.canvas.close()
        self.canvas = None

    def toggle(self):
        if self.enabled:
            self.disable()
        else:
            self.enable()

    def draw_canvas(self, canvas):
        paint = canvas.paint
        paint.color = 'fff'
        rect = canvas.rect

        SMALL_DIST   = 5
        SMALL_LENGTH = 10
        LARGE_DIST   = 25
        LARGE_LENGTH = 30
        irange = lambda start, stop, step: range(int(start), int(stop), int(step))
        paint.antialias = False
        for off, color in ((0, 'ffffffff'), (1, '000000ff')):
            paint.color = color

            # draw axis lines
            cx, cy = rect.center
            cxo = cx + off
            cyo = cy + off

            # draw ticks
            for tick_dist, tick_length in ((SMALL_DIST, SMALL_LENGTH),
                                           (LARGE_DIST, LARGE_LENGTH)):
                half = tick_length // 2
                # ticks to the left
                for x in irange(rect.left + off, cx - tick_dist + 1, tick_dist):
                    canvas.draw_line(x, cy - half, x, cy + half)
                # ticks to the right
                for x in irange(cxo + tick_dist - 1, rect.right + 1, tick_dist):
                    canvas.draw_line(x, cy - half, x, cy + half)
                # ticks above
                for y in irange(rect.top + off + 1, cy - tick_dist + 1, tick_dist):
                    canvas.draw_line(cx - half, y, cx + half, y)
                # ticks below
                for y in irange(cyo + tick_dist, rect.bot + 1, tick_dist):
                    canvas.draw_line(cx - half, y, cx + half, y)

    def on_mouse(self, event):
        self.check_mouse()

    def check_mouse(self):
        pos = ctrl.mouse_pos()
        if pos != self.last_pos:
            x, y = pos
            self.canvas.move(x - self.width // 2, y - self.height // 2)
            self.last_pos = pos

mouse_guide = MouseGuide(500, 500)
mouse_guide.enable()

mod = Module()
mod.list('mouse_cardinal', desc='cardinal directions for relative mouse movement')

def parse_cardinal(direction: str, distance: int) -> Tuple[bool, int]:
    x, y = ctrl.mouse_pos()
    if ' ' in direction:
        modifier, direction = direction.split(' ', 1)
        if modifier == 'minor':
            distance *= 5
        if modifier == 'major':
            distance *= 25
    if direction == 'west':
        return True, x - distance
    elif direction == 'east':
        return True, x + distance
    elif direction == 'north':
        return False, y - distance
    elif direction == 'south':
        return False, y + distance
    raise ValueError(f"unsupported cardinal direction: {direction}")

@mod.action_class
class Actions:
    def mouse_guide_enable():
        """Enable relative mouse guide"""
        mouse_guide.enable()

    def mouse_guide_disable():
        """Disable relative mouse guide"""
        mouse_guide.disable()

    def mouse_guide_toggle():
        """Toggle relative mouse guide"""
        mouse_guide.toggle()

    def mouse_cardinal(direction: str, distance: int) -> int:
        """Translate the current mouse position using a cardinal direction and a distance"""
        horiz, pos = parse_cardinal(direction, distance)
        return pos

    def mouse_cardinal_move_1d(direction: str, distance: int):
        """Move the mouse along a cardinal, e.g. 'move 1 left'"""
        x, y = ctrl.mouse_pos()
        horiz, pos = parse_cardinal(direction, distance)
        if horiz:
            x = pos
        else:
            y = pos
        ctrl.mouse_move(x, y)

    def mouse_cardinal_move_2d(dir1: str, dist1: int, dir2: str, dist2: str):
        """Move the mouse along a 2d cardinal, e.g. 'move 1 left 2 up'"""
        horiz1, pos1 = parse_cardinal(dir1, dist1)
        horiz2, pos2 = parse_cardinal(dir2, dist2)
        if horiz1 == horiz2:
            raise ValueError('cannot move twice along the same axis')
        x, y = pos1, pos2
        if horiz2:
            y, x = x, y
        ctrl.mouse_move(x, y)

ctx = Context()
ctx.lists['user.mouse_cardinal'] = [
    'north', 'west', 'south', 'east',
    'major north', 'major west', 'major south', 'major east',
    'minor north', 'minor west', 'minor south', 'minor east',
]
