# Algo

## Server

### Installing dependencies 
```bash
pip install -r requirements.txt
```

Start the server by 

```bash
python main.py
```

The server will then be run at  ``localhost:5000``

### API endpoints:

##### 0. Direction of the robot (d)
```NORTH```: 0

```EAST```: 2

```SOUTH```: 4

```WEST```: 6

##### 1. POST request to /path:
Sample json request body:  
```bash
{"obstacles" : 
    [
        {"x" : 5, "y" : 10, "id": 1, "d" : 2} 
    ]
}
```


Sample json response:

```{
    "data": {
        "commands": [
            "FR00",
            "FW01",
            "FW01",
            "FW01",
            "FW01",
            "FW01",
            "FL00",
            "FW01",
            "FW01",
            "FW01",
            "FL00",
            "SNAP1",
            "FIN"
        ],
        "distance": 29.0,
        "path": [
            {
                "d": 0,
                "s": -1,
                "x": 1,
                "y": 1
            },
            {
                "d": 2,
                "s": -1,
                "x": 3,
                "y": 3
            },
            {
                "d": 2,
                "s": -1,
                "x": 4,
                "y": 3
            },
            {
                "d": 2,
                "s": -1,
                "x": 5,
                "y": 3
            },
            {
                "d": 2,
                "s": -1,
                "x": 6,
                "y": 3
            },
            {
                "d": 2,
                "s": -1,
                "x": 7,
                "y": 3
            },
            {
                "d": 2,
                "s": -1,
                "x": 8,
                "y": 3
            },
            {
                "d": 0,
                "s": -1,
                "x": 10,
                "y": 5
            },
            {
                "d": 0,
                "s": -1,
                "x": 10,
                "y": 6
            },
            {
                "d": 0,
                "s": -1,
                "x": 10,
                "y": 7
            },
            {
                "d": 0,
                "s": -1,
                "x": 10,
                "y": 8
            },
            {
                "d": 6,
                "s": 1,
                "x": 8,
                "y": 10
            }
        ]
    },
    "error": null
}
```


##### 2. POST request to /image

The image is sent to the API as a file, thus no `base64` encoding required.

**Sample Request in Python**
```python3
response = requests.post(url, files={"file": (filename, image_data)})
```
- `image_data`: a `bytes` object

The API will then perform three operations:
1. Store the received file into the `/uploads` directory.
2. Use the model to identify the image.
3. Return the result as a `json` response.

**Sample json response**

```json
{
    "image_id": "D",
    "obstacle_id": 1
}
```

##### 3. POST request to /navigate

This will provide commands to the rpi for the obstacles to navigate around an obstacle.
The command process will be up to rpi side

**Sample Request in Python**
```python3
{
    "robot" : {"x" : 1, "y" : 1, "d" : 0}, 
    "obstacle" : {"x" : 6, "y" : 6}   
}
```

The API then return something like this:

```json
{
    "commands": [
        "FW01",
        "FW01",
        "FW01",
        "FR00",
        "SNAPE",
        "BL00",
        "FW01",
        "BL00",
        "BW01",
        "BR00",
        "FW01",
        "SNAPS",
        "BW01",
        "FL00",
        "FW01",
        "FR00",
        "BW01",
        "FR00",
        "SNAPW",
        "BL00",
        "BW01",
        "BL00",
        "BW01",
        "BW01",
        "BW01",
        "BW01",
        "BW01",
        "FL00",
        "SNAPN",
        "FIN"
    ]
}
```