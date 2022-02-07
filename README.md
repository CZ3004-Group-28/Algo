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
            "STOP"
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