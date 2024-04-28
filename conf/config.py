from dynaconf import Dynaconf
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
# parent_dir = os.path.dirname(current_dir)

setting_files = ["settings.yaml", ".secrets.yaml"]

config_file = os.environ.get("CONFIG_FILE")
if config_file:
    setting_files.append(config_file)
    print(f"Using config file: {config_file}")

settings = Dynaconf(
    envvar_prefix="COF",
    environments=True,
    load_dotenv=True,
    settings_files=setting_files,
    root_path=current_dir,
)
