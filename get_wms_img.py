import urllib.request

def get_wms_imgs(bbox, time, save_format):
    url = f'https://sh.dataspace.copernicus.eu/ogc/wms/eed4bff1-12d6-4792-92f6-8efb209d767e?REQUEST=GetMap&layers=CLOUD_THICKNESS&version=1.1.1&width={1700}&height={800}&srs=EPSG%3A4326&bbox={bbox}&TIME={time}'
    urllib.request.urlretrieve(url, save_format) 
    
def calculate_target_dimensions(bbox, max_dimension):
    """
    Calculate the target width and height based on the bounding box and a maximum dimension.

    Args:
        bbox (tuple): Bounding box in the format (min_x, min_y, max_x, max_y).
        max_dimension (int): The maximum allowed width or height for the image.

    Returns:
        tuple: The target width and height for the WMS request.
    """
    min_x, min_y, max_x, max_y = bbox

    # Calculate the width and height of the bounding box in degrees
    bbox_width = max_x - min_x
    bbox_height = max_y - min_y

    # Calculate the aspect ratio of the bounding box
    aspect_ratio = bbox_width / bbox_height

    # Calculate target dimensions based on max_dimension
    if bbox_width > bbox_height:
        # Width is greater, so set the width to max_dimension
        target_width = max_dimension
        target_height = int(target_width / aspect_ratio)
    else:
        # Height is greater, so set the height to max_dimension
        target_height = max_dimension
        target_width = int(target_height * aspect_ratio)

    return target_width, target_height

# Example usage
bbox = (19, 83, 27, 66)  # (min_x, min_y, max_x, max_y)
max_dimension = 1000  # Maximum allowed width or height (in pixels)

target_width, target_height = calculate_target_dimensions(bbox, max_dimension)
print(f"Target Width: {target_width}, Target Height: {target_height}")

    
get_wms_imgs('19,83,27,66', '2024-07-01T00:01:00Z/2024-09-31T00:00:00', 'input_frames/4.jpg')