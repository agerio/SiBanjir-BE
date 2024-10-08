import ftplib
import io
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class govapi(APIView):
    def get(self, request):
        # FTP server details
        ftp_server = "ftp.bom.gov.au"
        file_path = "/anon/gen/fwo/IDQ65448.txt"

        # Connect to the FTP server
        ftp = ftplib.FTP(ftp_server)
        ftp.login()  # Anonymous login

        # Use BytesIO for in-memory file storage
        with io.BytesIO() as mem_file:
            ftp.retrbinary(f"RETR {file_path}", mem_file.write)
            mem_file.seek(0)  # Go back to the beginning of the file

            # Read the downloaded content as text
            data = mem_file.read().decode('utf-8').splitlines()

        # Close the FTP connection
        ftp.quit()

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

        # Return the parsed data as a JSON response
        return Response(parsed_data, status=status.HTTP_200_OK)
