# gmusicchecker

This script checks your Google Play Music library for removed songs. Google is constantly updating its catalog and in the process removes older versions of songs from your library. However, it doesn't automatically add newer versions back to your library. This script creates a list of songs in your library on first run and compares the original list and new list on subsequent runs to let you know which songs have been removed.

Requires [gmusicapi](https://github.com/simon-weber/gmusicapi) which you can install with:
```
pip3 install gmusicapi
```

## Usage

Run the script with your Google username and password as command line arguments.

You can either `git clone` this repo and run the script like so:

```
git clone https://github.com/cjbassi/gmusicchecker
./path/to/script/gmusicchecker.py username password
```

Or you can run the script once-off by curling it directly to the python interpreter:

```
python3 <(curl https://raw.githubusercontent.com/cjbassi/gmusicchecker/master/gmusicchecker.py) username password
```

If you have 2-factor authentication (which you should :P) then you need to create an app-password [here](myaccount.google.com/apppasswords).

The script will create a `library.json` file on first run, which it will update with your current library. Subsequent runs will check for any removed songs which it will write to `removed_songs.txt` and then update `library.json` again.
