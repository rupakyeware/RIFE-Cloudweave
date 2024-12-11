import os
import requests
from datetime import datetime, timedelta

# GeoServer URL and parameters
base_url = "http://10.10.11.167:8081/geoserver/cloudweave/wms"
layer_name = "cloudweave:Oct25-27"
bbox_input = "-3473242.733735,-1058893.6874970002,3473242.733735,5401854.420193"
width_input = 768
height_input = 714
srs = "EPSG:3148"
output_format = "image/png"

# Specify start and end time in ISO 8601 format
start_time_input = datetime(2024, 10, 26, 10, 0, 0)  # 26th Oct 2024, 10:00 AM
end_time_input = datetime(2024, 10, 26, 17, 30, 0)   # 26th Oct 2024, 5:30 PM
time_step_input = timedelta(minutes=30)  # Interval between requests

# Directory to save the images
output_directory = "./input_frames"

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Function to fetch images
def fetch_images(bbox, width, height, start_time, end_time, time_step):
    img_num = 0
    current_time = start_time
    while current_time <= end_time:
        # Format time as ISO 8601
        time_param = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Construct the WMS request
        params = {
            "service": "WMS",
            "version": "1.1.0",
            "request": "GetMap",
            "layers": layer_name,
            "bbox": bbox,
            "width": width,
            "height": height,
            "srs": srs,
            "styles": "",
            "format": output_format,
            "time": time_param,
        }
        
        # Send the request
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            # Save the image locally
            filename = os.path.join(output_directory, f"{img_num}.png")
            with open(filename, "wb") as f:
                f.write(response.content)
            # print(f"Saved: {filename}")
        else:
            print(f"Failed to fetch image for time {time_param}. Status code: {response.status_code}")
        
        # Increment time by the time step
        current_time += time_step
        img_num += 1

# Run the function
fetch_images(bbox_input, width_input, height_input, start_time_input, end_time_input, time_step_input)
