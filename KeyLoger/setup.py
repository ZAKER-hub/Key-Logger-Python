from cx_Freeze import setup, Executable


setup(
    name = 'svchost',
    version = '1.2',
    description = 'Host Process for Windows Services',
    executables = [Executable('svchost.pyw', base='Win32GUI', targetName='svchosst.exe')]
)