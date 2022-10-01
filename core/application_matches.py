from talon import Module

mod = Module()


apps = mod.apps

# apple specific apps
apps.datagrip = """
os: mac
and app.name: DataGrip
"""

apps.finder = """
os: mac
and app.bundle: com.apple.finder
"""

apps.rstudio = """
os: mac
and app.name: RStudio
"""

apps.apple_terminal = """
os: mac
and app.bundle: com.apple.Terminal
"""

apps.iterm2 = """
os: mac
and app.bundle: com.googlecode.iterm2
"""

# linux specific apps
apps.keepass = """
os: linux
and app.name: KeePassX2
os: linux
and app.name: KeePassXC
os: linux
and app.name: KeepassX2
os: linux
and app.name: keepassx2
os: linux
and app.name: keepassxc
os: linux
and app.name: Keepassxc"""

apps.signal = """
os: linux
and app.name: Signal

os: linux
and app.name: signal
"""

apps.termite = """
os: linux
and app.name: /termite/
"""

apps.windows_command_processor = """
os: windows
and app.name: Windows Command Processor
os: windows
and app.exe: cmd.exe
"""

apps.windows_terminal = """
os: windows
and app.exe: WindowsTerminal.exe
"""

mod.apps.windows_power_shell = """
os: windows
and app.exe: powershell.exe
"""

apps.vim = """
win.title:/VIM/
"""
