"""Tobii eye tracker wrapper."""

import math
import sys


class EyeTracker:
    _instance = None

    @classmethod
    def get_connected_instance(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = cls(*args, **kwargs)
        if not cls._instance.is_connected:
            cls._instance.connect()
        return cls._instance

    def __init__(
        self,
        tobii_dll_directory,
        mouse=None,
        keyboard=None,
        windows=None,
    ):
        if not mouse or not keyboard or not windows:
            raise RuntimeError(
                "Must provide keyboard, mouse, and windows implementation. "
                "Import gaze_ocr.dragonfly or gaze_ocr.talon and use Mouse(), Keyboard(), and Windows()"
            )
        self._mouse = mouse
        self._keyboard = keyboard
        self._windows = windows
        # Attempt to load eye tracker DLLs.
        global clr, Action, Double, Host, GazeTracking
        try:
            import clr
            from System import Action, Double

            sys.path.append(tobii_dll_directory)
            clr.AddReference("Tobii.Interaction.Model")
            clr.AddReference("Tobii.Interaction.Net")
            from Tobii.Interaction import Host
            from Tobii.Interaction.Framework import GazeTracking

            self.is_mock = False
        except Exception:
            print("Eye tracking libraries are unavailable.")
            self.is_mock = True
        self._host = None
        self._gaze_point = None
        self._gaze_state = None
        self._screen_scale = (1.0, 1.0)
        self._monitor_size = windows.get_monitor_size()
        self._head_rotation = None
        self.is_connected = False

    def connect(self):
        if self.is_mock:
            return
        self._host = Host()

        # Connect handlers.
        screen_bounds_state = self._host.States.CreateScreenBoundsObserver()
        screen_bounds_state.Changed += self._handle_screen_bounds
        gaze_state = self._host.States.CreateGazeTrackingObserver()
        gaze_state.Changed += self._handle_gaze_state
        gaze_points = self._host.Streams.CreateGazePointDataStream()
        action = Action[Double, Double, Double](self._handle_gaze_point)
        gaze_points.GazePoint(action)
        head_pose = self._host.Streams.CreateHeadPoseStream()
        head_pose.Next += self._handle_head_pose
        self.is_connected = True
        print("Eye tracker connected.")

    def disconnect(self):
        if not self.is_connected:
            return
        self._host.DisableConnection()
        self._host = None
        self._gaze_point = None
        self._gaze_state = None
        self.is_connected = False
        print("Eye tracker disconnected.")

    def _handle_screen_bounds(self, sender, state):
        if not state.IsValid:
            print("Ignoring invalid screen bounds.")
            return
        bounds = state.Value
        monitor_size = self._windows.get_monitor_size()
        self._screen_scale = (
            monitor_size[0] / float(bounds.Width),
            monitor_size[1] / float(bounds.Height),
        )
        self._monitor_size = monitor_size

    def _handle_gaze_state(self, sender, state):
        if not state.IsValid:
            print("Ignoring invalid gaze state.")
            return
        self._gaze_state = state.Value

    def _handle_gaze_point(self, x, y, timestamp):
        self._gaze_point = (x, y, timestamp)

    def _handle_head_pose(self, sender, stream_data):
        pose = stream_data.Data
        self._head_rotation = (
            pose.HeadRotation.X,
            pose.HeadRotation.Y,
            pose.HeadRotation.Z,
        )
        self._head_position = (
            pose.HeadPosition.X,
            pose.HeadPosition.Y,
            pose.HeadPosition.Z,
        )

    def has_gaze_point(self):
        return (
            not self.is_mock
            and self._gaze_state == GazeTracking.GazeTracked
            and self._gaze_point
        )

    def get_gaze_point(self):
        if self.has_gaze_point():
            return (
                self._gaze_point[0] * self._screen_scale[0],
                self._gaze_point[1] * self._screen_scale[1],
            )
        else:
            return None

    def get_gaze_point_or_default(self):
        return self.get_gaze_point() or self._windows.get_foreground_window_center()

    def get_monitor_size(self):
        return self._monitor_size

    def print_gaze_point(self):
        if not self.has_gaze_point():
            print("No valid gaze point.")
            return
        print(f"Gaze point: ({self._gaze_point[0]:f}, {self._gaze_point[1]:f})")

    def move_to_gaze_point(self, offset=(0, 0)):
        gaze = self.get_gaze_point_or_default()
        x = max(0, int(gaze[0]) + offset[0])
        y = max(0, int(gaze[1]) + offset[1])
        self._mouse.move((x, y))

    def type_gaze_point(self, format):
        self._keyboard.type(format % self.get_gaze_point_or_default()).execute()

    def get_head_rotation_or_default(self):
        rotation = self._head_rotation or (0, 0, 0)
        if math.isnan(rotation[0]):
            rotation = (0, 0, 0)
        return rotation

    def get_head_position_or_default(self):
        position = self._head_position or (0, 0, 0)
        if math.isnan(position[0]):
            position = (0, 0, 0)
        return position
