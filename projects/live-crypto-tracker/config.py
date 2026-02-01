
# config.py


from haashi_pkg.utility.utils import Utility
from typing import Iterable


# helper function
def is_valid(user_res: Iterable[str]) -> bool:
    return any(res.strip() for res in user_res)


def configure_credentials(path: str = "user_data/credentials.json") -> None:

    print("\n\nSetup your credentials...")

    while True:

        api_key = input("\nEnter your CMC_API_KEY: ").strip()

        bot_tk = input("\nEnter your Telegram Bot Token: ").strip()
        chat_id = input("Enter your Telegram Chat ID: ").strip()

        valid = is_valid((api_key, bot_tk, chat_id))

        if not valid:
            print(
                "The above input fields cannot be empty! Please try again."
            )
            continue

        user_credentials: dict[str, str] = {
            "CMC_API_KEY": api_key,
            "Telegram_Bot_Token": bot_tk,
            "Telegram_Chat_ID": chat_id,
            "": "",
            "Date created": Utility().get_current_time(only_date=False)
        }

        Utility().save_json(data=user_credentials, path=path)

        print("\n\nCredentials saved successfully.")

        break
