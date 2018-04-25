# Convert flac to mp3

It's dump simple converter from *.flac to *.mp3 using [ffmpeg](https://www.ffmpeg.org)

## How to use

There is not `setup.py` (I'll add it in future) so you need to run it as pure python script

```bash
$ python main.py --help
Usage: main.py [options]

Options:
  -h, --help            show this help message and exit
  -s SOURCE_DIR, --source=SOURCE_DIR
                        Source directory, which will contain source *.cue and
                        *.flack files
  -f FFMPEG_BIN, --ffmpeg=FFMPEG_BIN
                        full path to ffmpeg binary
  -d, --delete          Delete source *.cue and *.flac files, Default = False
```