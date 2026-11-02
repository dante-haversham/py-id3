import argparse
from pathlib import Path
from pprint import pprint

from mutagen import File as MGFile

# from mutagen.mp3 import MP3


class Musicfile:
    def __init__(self, musicfile) -> None:
        self.filename = musicfile
        self.audio = MGFile(musicfile)
        self.tags = {}

    def get_keys(self):

        if self.filename is None:
            return

        self.audio = MGFile(self.filename, easy=True)


def check_args():
    filenames: list = []
    todo: str = ""
    tag: str = ""
    tagvalue: str = ""

    parser = argparse.ArgumentParser(
        description="Check and change id3v2 tags in mp3 files."
    )
    parser.add_argument("-f", "--filenames", nargs="+", type=str, help="file name")
    parser.add_argument("-a", "--action", type=str, help="action")
    parser.add_argument("-t", "--tag", type=str, help="tag name")
    parser.add_argument("-v", "--value", type=str, help="tag value")
    # parser.add_argument("value", type=str, help="tag value")

    args = parser.parse_args()

    for f in args.filenames:
        path = Path(f)
        if path.is_file():
            filenames.append(path)
        else:
            print(f"File {path} not found!")

    if args.action:
        todo = args.action

    if args.tag:
        tag = str(args.tag)
        if args.value is None:
            print("No value for tag given.")
        else:
            tagvalue = str(args.value)

    # if args.value:
    #    tagvalue = str(args.value)

    return todo, filenames, tag, tagvalue


if __name__ == "__main__":
    todo, filenames, tag, tagvalue = check_args()
    print(f"todo: {todo}\nfilename: {filenames}\ntag: {tag}")

    for f in filenames:
        msf = Musicfile(f)
        msf.get_keys()
        if todo in ["print", "p"]:
            pprint(dict(msf.audio), indent=4)
            print("-----------------------------------")
        if todo in ["write", "w"]:
            print(f"Writing {tag}: {tagvalue}")
            # msf.write(msf.id32mg[tag], tagvalue)
            msf.audio[tag] = tagvalue
            msf.audio.save()
