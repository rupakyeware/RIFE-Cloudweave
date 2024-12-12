import os
import requests
from datetime import datetime, timedelta

# GeoServer URL and parameters
base_url = "http://10.10.9.25:8080/geoserver/cloudweave/wcs"
layer_name = "cyc"
bbox_input = "4953717.340298529714,-1118889.974843325792,12245143.98726223782,5700582.732343434356"
width_input = 612
height_input = 572
srs = "EPSG:3857"
output_format = "image/png"

# Specify start and end time in ISO 8601 format
# start_time_input = datetime(2019, 5, 20, 15, 0, 0)  
# end_time_input = datetime(2019, 5, 20, 17, 0, 0)   
# time_step_input = timedelta(minutes=30)  # Interval between requests

# Directory to save the images
output_directory = "./input_frames"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

def fetch_images(bbox, width, height, start_time, end_time, time_step):
    img_num = 0
    current_time = start_time
    while current_time <= end_time:
        time_param = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        print('in')

        params = {
            "service": "WMS",
            "version": "1.1.1",
            "request": "GetMap",
            "layers": layer_name,
            "bbox": bbox,
            "width": width,
            "height": height,
            "srs": srs,
            "styles": "", 
            "format": output_format,
            "time": time_param,
            "dpi":96,
            "map_resolution":96,
            "transparent":True
        }
        
        print(current_time, end_time)
        
        # Send the request
        response = requests.get(base_url, params=params)
        print(response.url)
        print('out')
        if response.status_code == 200:
            filename = os.path.join(output_directory, f"{img_num}.png")
            with open(filename, "wb") as f:
                f.write(response.content)
        else:
            print(f"Failed to fetch image for time {time_param}. Status code: {response.status_code}")
        
        current_time += time_step
        img_num += 1

# Run the function
# fetch_images(bbox_input, width_input, height_input, start_time_input, end_time_input, time_step_input)