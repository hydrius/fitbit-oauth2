# Automatically OAuth for Fitbit-Python API

## Description

This script allows the user to automatically authorise fitbit. Please read below for instuctions on how to use the script
Further information can be seen at my website.

## Installation
The preferable method is:
git clone https://github.com/hydrius/

otherwise:
Download the file directly


## Usage

Once the file is downloaded, you need to put it in your working directory.

Below is a minimal working example:

```
from fitbit_oauth2 import FitbitWrapper

class FitbitDownloader(FitbitWrapper)

   def __init__():
      FitbitWrapper.__init__()
      print self.client._COLLECTION_RESOURCE("activities")

if __name__ == '__main__':
   fb = FitbitDownloader()

```

During first execution, the script asks for your client id and client secret. This then gets saved to a config file (config.ini) along with your tokens.

There are also options that can be passed into FitbitWrapper.

* client_id
* client_secret
* config_dir

The default is None, however you can specify the config directory if you want
to have a global config folder.

## Licence

MIT
