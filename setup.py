from cx_Freeze import setup, Executable

base = None    

executables = [Executable("main.py", base=base)]

packages = ["idna", "smtplib", "os", "urllib", "json", "time", "datetime"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "CryptoPuller",
    options = options,
    version = "1.4",
    description = " ",
    executables = executables
)
