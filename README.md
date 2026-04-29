# Timelapse Tool CLI

A quick cli tool that can turn a directory of images into a timelapse video. I mainly created it for my [ESP32 Plant Cam Project](https://github.com/okyang/esp32PlantCam).

## Setup
  
Install [uv](https://docs.astral.sh/uv/getting-started/installation/).

## Quick Start

Install the tool

```shell
uv tool install -e .
```

Then go ahead and run the tool:

```shell
uv timelapse-tool-cli <path_to_images_folder> --fps 20
```

Get help:

```shell
uv timelapse-tool-cli --help
```

For example:

```shell
okyang@okyang-Laptop-16-AMD-Ryzen-7040-Series:~/code/my-full-stack$ timelapse-tool-cli --help
Usage: timelapse-tool-cli [OPTIONS] IMAGE_DIR

  Create a timelapse video from a directory of images.

  IMAGE_DIR is the path to the directory containing your images.

Options:
  -o, --output PATH             Output video filename. Defaults to
                                'timelapse.mp4'
  -f, --fps INTEGER             Frames per second for the video. Defaults to
                                10.
  -d, --darkframe-perc INTEGER  Dark frame threshold percentage. Frames with
                                average brightness below this are filtered.
                                Defaults to 20.
  --help                        Show this message and exit.
```

## Local Development

Create a virtual environment:

```shell
uv venv
```

Run main script with 20 frames per second (default 10)

```shell
uv run src/main.py <path_to_images_folder> -f 20
```

Example output:

```shell
(timelapse-tool-cli) okyang@okyang-Laptop-16-AMD-Ryzen-7040-Series:~/code/timelapse-tool-cli$ uv run src/main.py /home/okyang/Pictures/plant_cam -f 20
🎬 Creating timelapse video from images in: /home/okyang/Pictures/plant_cam
📸 Found 1185 images
🔧 Video dimensions: 1600x1200
⚙️  FPS: 20, Dark frame threshold: 20%
🎥 Processing frames: 100%|█████████████████████████████████████████████████████████████████| 1185/1185 [00:14<00:00, 83.45frame/s]
✅ Video created successfully: timelapse.mp4
📊 Video size: 127.13 MB
```

## Reference

- [python uv cli tool](https://note.nkmk.me/en/python-uv-cli-tool/)
