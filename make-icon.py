from pathlib import Path
from PIL import Image


def main(filename):
    filename = Path(filename)
    img = Image.open(filename)
    img.save(filename.with_suffix('.ico'), format='ICO', sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (256, 256)])


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser('make-icon.py')
    parser.add_argument('filename')
    args = parser.parse_args()
    main(args.filename)
