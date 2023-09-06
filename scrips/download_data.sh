#!/bin/bash

# Get yesterday's date
DATE=$(date -d "yesterday" +"%Y-%m-%d")

# Define the URL and file name
URL="https://github.com/chenditc/investment_data/releases/download/${DATE}/qlib_bin.tar.gz"
FILENAME="qlib_bin.tar.gz"

# Define the destination directory
DEST_DIR=~/.qlib/qlib_data/invest

# Remove the old file if it exists
if [ -f $FILENAME ]; then
    rm $FILENAME
fi

# Download the file in the background, with a timeout of 60 seconds and up to 10 retries
wget -b -c -t 10 -T 60 $URL -O $FILENAME

# Get the PID of the wget process
WGET_PID=$!

# Wait for the download to complete
while kill -0 $WGET_PID 2>/dev/null; do
    sleep 1
done

# Check if the file is downloaded completely
if wget -q --spider $URL; then
    # Extract the file to the destination directory
    tar -zxvf $FILENAME -C $DEST_DIR --strip-components=2
else
    echo "The file is not downloaded completely, please check the network connection and try again."
    exit 1
fi

# Clean up the downloaded file
rm $FILENAME

# Remove wget-log file
rm wget-log*

# Print completion message
echo "Script execution completed."
