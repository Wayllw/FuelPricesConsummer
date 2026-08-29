import DataCollector
import time


def main():
    DataCollector.main()

    import AWSUploader
    import Notifier
    import Publisher

    print("Data collected")
    Publisher.main()
    print("Publish started")
    AWSUploader.main()
    print("AWS uploader started")
    Notifier.main()
    print("Notifier started")

if __name__ == "__main__":
    main()