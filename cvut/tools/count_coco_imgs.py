import json
import argparse


# ------------------------------------------------------------------------------
#  ArgumentParser
# ------------------------------------------------------------------------------
parser = argparse.ArgumentParser("Count #images from the COCO-format json file")

parser.add_argument("json", type=str, help="Json file")

args = parser.parse_args()


# ------------------------------------------------------------------------------
#  Main execution
# ------------------------------------------------------------------------------
def main():
    with open(args.json, 'r') as fp:
        data = json.load(fp)
    print(f"Number of images: {len(data['images'])}")


if __name__ == '__main__':
    main()
