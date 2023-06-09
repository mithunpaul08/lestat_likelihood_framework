import argparse

parser=argparse.ArgumentParser(description="test")
parser.add_argument("--prompt")
args=parser.parse_args()

print(f"value of prompt is {args.prompt}")