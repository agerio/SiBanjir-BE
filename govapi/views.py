from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import *
from .serializer import *
import ftplib
import io
from bs4 import BeautifulSoup
from decimal import Decimal


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

class GovAPI(APIView):
    def get(self, request):
        flood_watches = FloodWatch.objects.all()
        serializer = FloodWatchSerializer(flood_watches, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class GovAPIRefresh(APIView):
    def get(self, request):
        ftp_server = "ftp.bom.gov.au"
        file_path1 = "/anon/gen/fwo/IDQ60005.html"
        file_path2 = "/anon/gen/fwo/IDQ65448.txt"

        ftp = ftplib.FTP(ftp_server)
        ftp.login()

        with io.BytesIO() as mem_file:
            ftp.retrbinary(f"RETR {file_path1}", mem_file.write)
            mem_file.seek(0)
            html_data = mem_file.read().decode('utf-8')

            ftp.retrbinary(f"RETR {file_path2}", mem_file.write)
            mem_file.seek(0)
            csv_data = mem_file.read().decode('utf-8').splitlines()

        ftp.quit()

        soup = BeautifulSoup(html_data, 'html.parser')
        rows = soup.find_all('tr')

        stn_data = {}
        for row in rows:
            metadata = row.find(string=lambda text: text and 'METADATA' in text)
            if metadata:
                parts = metadata.split(',')
                stn_num = int(parts[1])
                area_id = int(parts[8][3:])

                cells = row.find_all('td')
                
                obs_time = cells[1].get_text(strip=True) if len(cells) > 1 else ""
                hgt = float(cells[2].get_text(strip=True).rstrip('^')) if len(cells) > 2 and cells[2].get_text(strip=True) else None
                tendency = cells[3].get_text(strip=True) if len(cells) > 3 else ""
                classif = cells[5].get_text(strip=True) if len(cells) > 5 else "unknown"

                stn_data[stn_num] = {
                    'area_id': area_id,
                    'obs_time': obs_time,
                    'hgt': hgt,
                    'tendency': tendency,
                    'classif': classif,
                }

        parsed_data = []
        for line in csv_data:
            if line.strip() and not line.startswith("# HEADER:"):
                values = line.split(",")

                if (not values[0].strip().isnumeric()): continue
                stn_num = int(values[0].strip())

                if (not is_float(values[11].strip()) or not is_float(values[12].strip())): continue
                if (stn_num not in stn_data): continue

                entry = {
                    "stn_num": int(stn_num),
                    "name": values[2].strip(),
                    "long": Decimal(values[11].strip()),
                    "lat": Decimal(values[12].strip()),
                    'area_id': stn_data[stn_num]['area_id'],
                    'obs_time': stn_data[stn_num]['obs_time'],
                    'hgt': stn_data[stn_num]['hgt'],
                    'tendency': stn_data[stn_num]['tendency'],
                    'classif': stn_data[stn_num]['classif'],
                }
                parsed_data.append(entry)

        for data in parsed_data:
            # Update existing records or create new ones
            FloodWatch.objects.update_or_create(
                stn_num=data['stn_num'],
                defaults={
                    'name': data['name'],
                    'long': data['long'],
                    'lat': data['lat'],
                    'hgt': data['hgt'],
                    'classif': data['classif'],
                    'obs_time': data['obs_time'],
                    'area_id': data['area_id']
                }
            )

        return Response({"message": "Data has been successfully updated."}, status=status.HTTP_200_OK)


class old_govapi(APIView):
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
