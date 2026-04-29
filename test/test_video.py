import os
from pathlib import Path
import pytest

import cv2
import numpy as np
from src.video import TimelapseTool


def test_video_creation_with_sample_data(tmp_path):
    """_summary_

    Args:
        tmp_path (pathlib.Path): built-in pytest fixture
    """
    # create dummy images to use as input
    image_paths: list[os.PathLike] = []
    for i in range(3):
        img_file = tmp_path / f"img{i}.jpg"
        bright = np.full((10, 10, 3), 255, dtype=np.uint8)
        cv2.imwrite(str(img_file), bright)
        image_paths.append(img_file)

    # test inputs
    output: Path = tmp_path / "timelapse.mp4"

    # testing start here
    t = TimelapseTool(image_paths, output)
    t.create_video()
    assert output.exists()

    # cleanup
    os.remove(output)


def test_filter_missing_paths(tmp_path):
    """

    Args:
        tmp_path (pathlib.Path): built-in pytest fixture
    """
    # create dummy test image files (bright, so they won't be treated
    # as dark frames and filtered out later)
    img1 = tmp_path / "a.jpg"
    img2 = tmp_path / "b.jpg"
    bright = np.full((10, 10, 3), 255, dtype=np.uint8)
    cv2.imwrite(str(img1), bright)
    cv2.imwrite(str(img2), bright)

    # add a missing path "<path>/missing.jpg" to the list
    paths = [img1, img2, tmp_path / "missing.jpg"]
    output = tmp_path / "out.mp4"

    # initialization should drop the missing entry
    t = TimelapseTool(paths, output)
    assert all(os.path.exists(p) for p in t.image_paths)
    assert str(tmp_path / "missing.jpg") not in t.image_paths

    # testing starts here
    # writing a video should succeed and create the file
    t.create_video()
    assert output.exists()

    # TODO: actually check the number of frames in the video


def test_no_valid_images_raises():
    # should raise a ValueError when TimelapseTool
    # is initialized with a empty list of image paths
    with pytest.raises(ValueError):
        TimelapseTool([], Path("foo.mp4"))
