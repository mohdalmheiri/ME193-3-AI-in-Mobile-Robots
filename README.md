# ME193-3: AI in Mobile Robots

Coursework and projects for ME193-3, AI in Mobile Robots. Each assignment
lives in its own folder with its own README covering that assignment's
setup and write-up — this top-level README is just an index.

## Assignments

| Folder | Assignment | Summary |
|---|---|---|
| [`Pose Race/`](./Pose%20Race) | Pose Race (HW1) | Control a LEGO car with arm gestures tracked via webcam + MediaPipe Pose |

*(Add a new row here each time a new assignment folder is added.)*

## Repo structure

```
.
├── README.md              # this file — index of all assignments
├── Pose Race/
│   ├── README.md           # assignment-specific setup + write-up
│   ├── arm_control_car.py
│   └── find_devices.py
└── ...                     # future assignments go here, one folder each
```

## Setup (general)

Each assignment folder may have its own dependencies — check that folder's
README for exact install steps. In general:

```
python3 -m venv my_env
source my_env/bin/activate  # On Mac/Linux
# or
my_env\Scripts\activate     # On Windows

pip install --upgrade pip
```
