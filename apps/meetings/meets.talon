# meet.talon
app: google meet
-

toggle (mute|microphone):
    user.toggle_microphone()

toggle (video|camera):
    user.toggle_camera()

toggle chat:
    user.toggle_chat()

toggle people:
    user.toggle_people()

toggle captions:
    user.toggle_captions()

toggle hand:
    user.toggle_hand()

(leave meeting|go back):
    user.leave_meeting()