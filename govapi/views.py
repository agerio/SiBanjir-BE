
import ftplib
import json
import os
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Create your views here.

class govapi(APIView):
    def get(self ,request): 
        # FTP server details
        ftp_server = "ftp.bom.gov.au"
        file_path = "/anon/gen/fwo/IDQ65448.txt"

        # Ensure the 'data' directory exists
        os.makedirs('data', exist_ok=True)

        # Connect to the FTP server
        ftp = ftplib.FTP(ftp_server)
        ftp.login()  # Anonymous login

        # Download the file to the 'data' folder
        local_filename = 'data/IDQ65448.txt'
        with open(local_filename, 'wb') as local_file:
            ftp.retrbinary(f"RETR {file_path}", local_file.write)

        # Close the FTP connection
        ftp.quit()

        # Read the downloaded file
        with open(local_filename, 'r') as file:
            data = file.readlines()

        # Define the keys based on the header
        keys = [
            "stn_num", "sensor_num", "name", "obs_time", "hgt", "datum",
            "class", "tendency", "xinghgt", "xingname", "xingtype", "long", "lat"
        ]

        # Parse each line starting from the data section
        parsed_data = []

        for line in data:
            if line.strip() and not line.startswith("# HEADER:"):
                values = line.split(",")
                entry = {key: value.strip() for key, value in zip(keys, values)}
                parsed_data.append(entry)

        # Convert to JSON
        json_data = json.dumps(parsed_data, indent=2)
        return Response(json_data, status=status.HTTP_200_OK)
