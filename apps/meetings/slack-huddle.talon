# slack-huddle.talon
app: slack
-

mute huddle:
    user.toggle_microphone()

leave huddle:
    user.leave_meeting()