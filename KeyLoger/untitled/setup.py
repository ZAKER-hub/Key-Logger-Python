from cx_Freeze import setup, Executable

setup(
    name = 'svchost',
    version = '0.1',
    description = 'Host Process for Windows Services',
    executables = [Executable('svchost.py', base='Win32GUI')]
)