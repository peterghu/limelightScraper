# limelightScraper

Simple Python script to download your video catalogue from Limelight.

### Requirements
Python 3+
Your Limelight API credentials - you can view these on the Limelight platform settings page

### Usage and Setup
Go to 'config.ini' and set your 'organization', 'accesskey' and 'secretkey' values. Update the key expiry time too if needed.
There are other settings to tweak which are pretty self-explanatory, see 'Settings' for more information.

You can then run the script simply as follows:
  `python .\limelightScraper.py`

### Settings
* `output` - Folder to download to
* `printCatalogueToJson` - print your Limelight catalogue as JSON to a text file
* `disableDownload` - don't download, use if you just want to test if your connection is working
* `downloadDelay` - time in seconds to wait between downloads
* `downloadStartPoint` - number of videos to skip in your catalogue to before starting downloads, ie. 5 would skip the first five videos 
* `maxDownloads` - number of max videos to download


### Troubleshooting
TBD

### Future Changes
TBD
