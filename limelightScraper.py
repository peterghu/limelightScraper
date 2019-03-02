import requests
import hmac
import hashlib
import base64
import json
import urllib
import sys
import pathlib
import re
import os
import contextlib
import time
from urllib import parse

import config

def main():
    videoLibraryJson = sendGetReq(f"http://api.video.limelight.com/rest/v3/organizations/{config.ORGANIZATION_ID}/media/search")
    
    if videoLibraryJson is None:
        print("Please check config and try again.")
        return None

    if config.PRINT_MEDIA_LIST == 1:
        printLibraryJson(videoLibraryJson)

    downloadLibrary(videoLibraryJson)


def silentRemove(filename):
    with contextlib.suppress(FileNotFoundError):
        os.remove(filename)

def printLibraryJson(videoLibraryJson):
    limelightJsonPath = pathlib.Path(__file__).parent / 'limelightVideoCatalogue.json'
    silentRemove(limelightJsonPath)

    with open(limelightJsonPath, "w") as f:
        json.dump(videoLibraryJson, f)
        f.close()
        print("JSON dump of Limelight video catalogue has been saved to:", limelightJsonPath)

def downloadLibrary(videoLibraryJson):
    maxIterCounter  = 0
    notFoundArray   = []

    #Download each video
    if videoLibraryJson['total_results'] > 0:
        for video in videoLibraryJson['media_list']:
            
            maxIterCounter += 1
            if maxIterCounter == config.MAX_DOWNLOADS:
                break
            if maxIterCounter < config.START_ITERATION:
                continue
            else:
                time.sleep(config.DOWNLOAD_DELAY)

            mediaJson = sendGetReq(f"http://api.video.limelight.com/rest/organizations/{config.ORGANIZATION_ID}/media/{video['media_id']}/source")
            if (mediaJson):
                mediaUrl = mediaJson['url']
                extension = str(mediaJson['source_details']['container_type']).lower()
                sourceFilename = mediaJson['source_details']['original_file_name'] + '.' + extension
                downloadUrl(mediaUrl, sourceFilename, config.OUTPUT_PATH)
            else:
                notFoundArray.append(video['original_filename'])
    
    print("\nDone!")
    if (len(notFoundArray) > 0 ):
        print(f"Files not found: {len(notFoundArray)}")
        print(notFoundArray)

def downloadUrl(url, sourceFilename, outputDir):
    outputDir   = pathlib.Path(__file__).parent / outputDir 
    sourceFile  = outputDir / sourceFilename
    tempFile    = outputDir / 'temp.dat'
    totalLength = None

    os.makedirs(os.path.dirname(tempFile), exist_ok=True)
    silentRemove(tempFile)

    with open(tempFile, "wb") as f:

        response    = requests.get(url, stream=True)
        totalLength = response.headers.get('content-length')
        
        if totalLength is None:
            f.write(response.content) 
        else:
            if config.DISABLE_DOWNLOAD == 1:
                return
            dl = 0
            totalLength = int(totalLength)
            print(f"\nDownloading to {sourceFile}")
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                progress = int(50 * dl / totalLength)
                sys.stdout.write("\r[%s%s]  %s %% complete " % ('=' * progress, ' ' * (50-progress), progress / 0.5) )    
                sys.stdout.flush()
    if totalLength:
        silentRemove(sourceFile) #don't care if we downloaded it before
        os.rename(tempFile, sourceFile)

def sendGetReq(endpoint):
    obj       = parse.urlsplit(endpoint)
    signature = f"get|{obj.netloc}|{obj.path}|"

    params = {
        'access_key': config.ACCESS_KEY,
        'expires'   : config.KEY_EXPIRES,
        'signature' : ''
    }

    for key, value in params.items():
        if value != '':
            signature += str(key) + "=" + str(value) + "&"
    signature = signature[:-1]

    #signature += parse.urlencode(params) #can't url encode before hashing!
    newHash = base64.b64encode(
        hmac.new(config.SECRET_KEY.encode("ascii"), signature.encode("ascii"), digestmod=hashlib.sha256).digest()
    )
    params["signature"] = newHash.decode("ascii")
    
    #testGetReq(endpoint, params)
    response = requests.get(endpoint,params=params, timeout=5)

    if response.status_code != 200:
        print("Cannot download at: '" + endpoint + "', Error", str(response.status_code), ":", 
              str(response.json()['errors'][0]) )
        return None
    else:
        return response.json()

#Test code to see how GET URL looks
def testGetReq(endpoint, params):
    response = requests.Request('get',endpoint,params=params).prepare().url
    print(response)


if __name__ == '__main__':
    main()