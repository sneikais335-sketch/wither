import json
import os

class LanguageManager:
    def __init__(self):
        self.current = "en"
        self.strings = {}
        # Will load base path correctly when instantiated in app
        self.base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "i18n")

    def load(self, code: str):
        try:
            with open(os.path.join(self.base_path, f"{code}.json"), encoding="utf-8") as f:
                self.strings = json.load(f)
            self.current = code
        except FileNotFoundError:
            print(f"Error: Language file for {code} not found.")
            if code != "en":
                self.load("en") # fallback

    def t(self, key: str) -> str:
        # Support nested keys: t("days.Monday")
        keys = key.split(".")
        val = self.strings
        for k in keys:
            if isinstance(val, dict):
                val = val.get(k, key)
            else:
                return key # Path broken
        return str(val) if not isinstance(val, dict) else key

    def switch(self, code: str, app_instance):
        self.load(code)
        if hasattr(app_instance, "refresh_all_texts"):
            app_instance.refresh_all_texts()
