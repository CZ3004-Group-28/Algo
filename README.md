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

### Miscellaneous
- Raw images from uploaded from the Raspberry Pi are stored at the `uploads` folder.
- After calling the `image/` endpoint, the annotated image (with bounding box and label) is stored in the `runs` folder.
- After calling the `stitch/` endpoint, the stitched image is located at `runs/stitched.jpg`

### API endpoints:

##### 0. Direction of the robot (d)
```NORTH```: 0

```EAST```: 2

```SOUTH```: 4

```WEST```: 6

##### 1. POST request to /path:

+) Obstacles: the list of obstacles that need to navigate

+) big_turn: 0 -> turn 3-1; 1 -> turn 4-2

Sample json request body:  
```bash
{
    "obstacles":
    [
        {
            "x": 4,
            "y": 11,
            "id": 1,
            "d": 4
        },
        {
            "x": 8,
            "y": 18,
            "id": 2,
            "d": 4
        },
        {
            "x": 9,
            "y": 6,
            "id": 3,
            "d": 0
        },
        {
            "x": 16,
            "y": 11,
            "id": 4,
            "d": 6
        },
        {
            "x": 16,
            "y": 19,
            "id": 5,
            "d": 4
        }
    ], 
    "big_turn" : 1
}
```


Sample json response:

```{
    "data": {
        "commands": [
            "FR30",
            "BS30",
            "FL30",
            "SNAP1",
            "FR30",
            "BS20",
            "FL30",
            "FS10",
            "SNAP2",
            "BS50",
            "FR30",
            "FS10",
            "SNAP4",
            "BL30",
            "FS30",
            "SNAP3",
            "BS20",
            "BL30",
            "BS10",
            "BL30",
            "FS10",
            "SNAP5",
            "FIN"
        ],
        "distance": 46.0,
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
                "x": 5,
                "y": 3
            },
            {
                "d": 2,
                "s": -1,
                "x": 2,
                "y": 3
            },
            {
                "d": 0,
                "s": 1,
                "x": 4,
                "y": 7
            },
            {
                "d": 2,
                "s": -1,
                "x": 8,
                "y": 9
            },
            {
                "d": 2,
                "s": -1,
                "x": 6,
                "y": 9
            },
            {
                "d": 0,
                "s": -1,
                "x": 8,
                "y": 13
            },
            {
                "d": 0,
                "s": 2,
                "x": 8,
                "y": 14
            },
            {
                "d": 0,
                "s": -1,
                "x": 8,
                "y": 9
            },
            {
                "d": 2,
                "s": -1,
                "x": 12,
                "y": 11
            },
            {
                "d": 2,
                "s": 4,
                "x": 13,
                "y": 11
            },
            {
                "d": 4,
                "s": -1,
                "x": 9,
                "y": 13
            },
            {
                "d": 4,
                "s": 3,
                "x": 9,
                "y": 10
            },
            {
                "d": 4,
                "s": -1,
                "x": 9,
                "y": 12
            },
            {
                "d": 6,
                "s": -1,
                "x": 11,
                "y": 16
            },
            {
                "d": 6,
                "s": -1,
                "x": 12,
                "y": 16
            },
            {
                "d": 0,
                "s": -1,
                "x": 16,
                "y": 14
            },
            {
                "d": 0,
                "s": 5,
                "x": 16,
                "y": 15
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
    ],
    "path": [
        {
            "d": 0,
            "s": -1,
            "x": 1,
            "y": 1
        },
        {
            "d": 0,
            "s": -1,
            "x": 1,
            "y": 2
        },
        {
            "d": 0,
            "s": -1,
            "x": 1,
            "y": 3
        },
        {
            "d": 0,
            "s": -1,
            "x": 1,
            "y": 4
        },
        {
            "d": 2,
            "s": 1,
            "x": 3,
            "y": 6
        },
        {
            "d": 4,
            "s": -1,
            "x": 1,
            "y": 8
        },
        {
            "d": 4,
            "s": -1,
            "x": 1,
            "y": 7
        },
        {
            "d": 6,
            "s": -1,
            "x": 3,
            "y": 9
        },
        {
            "d": 6,
            "s": -1,
            "x": 4,
            "y": 9
        },
        {
            "d": 4,
            "s": -1,
            "x": 6,
            "y": 11
        },
        {
            "d": 4,
            "s": 1,
            "x": 6,
            "y": 10
        },
        {
            "d": 4,
            "s": -1,
            "x": 6,
            "y": 11
        },
        {
            "d": 2,
            "s": -1,
            "x": 8,
            "y": 9
        },
        {
            "d": 2,
            "s": -1,
            "x": 9,
            "y": 9
        },
        {
            "d": 4,
            "s": -1,
            "x": 11,
            "y": 7
        },
        {
            "d": 4,
            "s": -1,
            "x": 11,
            "y": 8
        },
        {
            "d": 6,
            "s": 1,
            "x": 9,
            "y": 6
        },
        {
            "d": 0,
            "s": -1,
            "x": 11,
            "y": 4
        },
        {
            "d": 0,
            "s": -1,
            "x": 11,
            "y": 3
        },
        {
            "d": 2,
            "s": -1,
            "x": 9,
            "y": 1
        },
        {
            "d": 2,
            "s": -1,
            "x": 8,
            "y": 1
        },
        {
            "d": 2,
            "s": -1,
            "x": 7,
            "y": 1
        },
        {
            "d": 2,
            "s": -1,
            "x": 6,
            "y": 1
        },
        {
            "d": 2,
            "s": -1,
            "x": 5,
            "y": 1
        },
        {
            "d": 2,
            "s": -1,
            "x": 4,
            "y": 1
        },
        {
            "d": 0,
            "s": 1,
            "x": 6,
            "y": 3
        }
    ]
}
```

##### 4. POST request to /stitch
This will trigger the `stitch_image()` function.
- all images found in the `run/` directory will be stitched together and saved at `run/stitched.jpg`
