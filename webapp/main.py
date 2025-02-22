import pathlib
import time

def main():
    static_path = pathlib.Path(__file__).parent / "static"
    print(f"Static path: {static_path}")
    for f in static_path.walk():
        print(f)
    print("Hello from webapp!")
    while True:
        print("Running...")
        time.sleep(1)


if __name__ == "__main__":
    main()
