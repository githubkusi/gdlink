# Handle Google Drive links
If you sync Google Drive files to your local drive (e.g with Insync), Google Drive links unfortunately are not represented as proper file system links but as gdlink file, which contain a hash to the target file

## Usage
Get path to original file


    gdlink myfile.gdlink


Change to folder containing the target file

    cdgdlink myfile.gdlink


## Installation
Install gdlink executable

    pipx install .

Append to your .bashrc or .zshrc

    function cdgdlink()
    {
        p=$(gdlink --parent "$1")
        cd "$p"
    }

## First run

1. Go to https://console.cloud.google.com
2. New project "gdlink"
3. Enable "Google Drive API"
4. Credentials -> Create OAuth 2.0 Client ID, download client_secret.json file
5. gdlink --client-secret client_secret.json 

