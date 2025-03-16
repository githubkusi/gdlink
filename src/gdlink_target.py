import argparse
import os
import json

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# Google Drive API scopes
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

CONFIG_PATH = "~/.gdlink-target/config.json"
TOKEN_PATH = "~/.gdlink-target/token.json"


def read_gdlink_file_id(file_path):
    """Read JSON data from a file and extract the file_id."""
    with open(file_path, "r") as file:
        data = json.load(file)
    return data.get("file_id")


def authenticate_drive():
    """Authenticate using OAuth 2.0 and return Google Drive service."""
    creds = None
    token_file = os.path.expanduser(TOKEN_PATH)

    # Load saved credentials if they exist
    if os.path.exists(token_file):
        with open(token_file, "r") as token:
            creds_data = json.load(token)
            creds = Credentials.from_authorized_user_info(creds_data, SCOPES)

    # If credentials are not available or invalid, authenticate
    if not creds:
        print("You need to connect with your Google Drive first, see readme")
        exit(-1)

    return build("drive", "v3", credentials=creds)


def client_secret(client_secret_file_path):
    token_file = os.path.expanduser(TOKEN_PATH)
    flow = InstalledAppFlow.from_client_secrets_file(client_secret_file_path, SCOPES)
    creds = flow.run_local_server(port=0)

    # create "~/.gdlink-target"
    os.makedirs(os.path.dirname(token_file), exist_ok=True)

    # Save credentials for future use
    with open(token_file, "w") as token:
        token.write(creds.to_json())


def get_actual_file_id(service, file_id):
    """Get the actual file ID if it's a shortcut."""
    file_metadata = service.files().get(fileId=file_id, fields="id, name, mimeType, shortcutDetails").execute()

    # Check if the file is a shortcut
    if "shortcutDetails" in file_metadata:
        return file_metadata["shortcutDetails"]["targetId"]  # Get the target file ID

    return file_id  # Return the original ID if not a shortcut


def get_file_path(service, file_id):
    """Get the relative path of a file in Google Drive."""
    file_metadata = service.files().get(fileId=file_id, fields="id, name, parents").execute()

    path = [file_metadata["name"]]
    parent_id = file_metadata.get("parents", [None])[0]

    while parent_id:
        parent_metadata = service.files().get(fileId=parent_id, fields="id, name, parents").execute()
        path.insert(0, parent_metadata["name"])
        parent_id = parent_metadata.get("parents", [None])[0]

    return "/".join(path)


def get_gd_root():
    with open(os.path.expanduser(CONFIG_PATH), "r") as config_file:
        config = json.load(config_file)
    return config['gd_root']


def main():
    parser = argparse.ArgumentParser(description="Target folder of gdlink file")
    parser.add_argument("gdlink_file_path", help="Path to gdlink file")
    parser.add_argument("--parent", action='store_true', help="Return parent directory")
    parser.add_argument("--client_secret", action='store_true', help="Google Drive OAuth2.0 client-secret file for initial authentication")
    args = parser.parse_args()

    if args.client_secret:
        client_secret_file_path = args.gdlink_file_path
        client_secret(client_secret_file_path)
        print("Done, you can now use gdlink")
        exit(-1)

    file_id = read_gdlink_file_id(args.gdlink_file_path)

    """Main function to resolve a Google Drive shortcut and get the target path."""
    service = authenticate_drive()

    # Get the actual file ID if it's a shortcut
    actual_file_id = get_actual_file_id(service, file_id)
    # print(f"Actual File ID: {actual_file_id}")

    # Get the relative path of the target file
    relative_path = get_file_path(service, actual_file_id)

    cleaned_path = "/".join(relative_path.split("/")[1:])
    if args.parent:
        cleaned_path = "/".join(cleaned_path.split("/")[:-1])

    print(os.path.join(get_gd_root(), cleaned_path))


if __name__ == "__main__":
    main()
