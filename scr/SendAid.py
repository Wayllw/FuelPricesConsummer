import DataCollector

def main():
    DataCollector.main()

    import AWSUploader
    import Notifier
    import Publisher
    import Telegram_Conversation

    print("Data collected")
    Publisher.main()
    print("Publish started")
    AWSUploader.main()
    print("AWS uploader started")
    Notifier.main()
    print("Notifier started")
    Telegram_Conversation.main()
    print("Telegram started")

if __name__ == "__main__":
    main()