"""Input a bunch of images, generate a timelapse video

- Sorts the images by modified time
"""

import os
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from tqdm import tqdm


MAX_FRAME_SIZE = 4096  # max width or height in pixels
PROCESSING_TIMEOUT = 300  # 5 minutes in seconds


class TimelapseTool:
    """TimelapseTool takes a list of image paths and combines them into mp4 video.

    Methods
    -------
    create_video(image_paths, video_name, fps=10, darkframe_perc=20)
        processes the frames and creates the video.
    _isDarkFrame(frame)
        processes a single frame and determines if it is a dark frame.
        useful for filtering out dark frames.
    """

    def __init__(
        self,
        image_paths: list[Path],
        video_name: Path,
        fps=10,
        darkframe_perc=20,
    ):
        """
        Args:
            image_paths (list[os.PathLike]): list of image files to process
            video_name (os.PathLike | str): the output name of the video file
            fps (int, optional): _description_. Defaults to 10.
            darkframe_perc (int, optional): _description_. Defaults to 20.

        Raises:
            ValueError: _description_
            ValueError: _description_
        """
        # list of images
        self.image_paths: list[os.PathLike | str] = [
            p for p in image_paths if os.path.exists(p)
        ]
        self.video_name: os.PathLike = video_name
        self.fps: int = fps
        self.darkframe_perc: int = darkframe_perc

        if not self.image_paths:
            raise ValueError("no valid image files provided")

        # sort ascending (earliest to latest photo)
        self.image_paths.sort(key=lambda path: os.stat(path).st_mtime)

        # determine frame size from first image
        frame: np.ndarray[Any, np.dtype[np.integer[Any] | np.floating[Any]]] | None = (
            cv2.imread(self.image_paths[0])
        )

        if frame is None:
            raise ValueError(f"Could not read image: {self.image_paths[0]}")

        self.height, self.width, self.layers = frame.shape

        if self.width > MAX_FRAME_SIZE or self.height > MAX_FRAME_SIZE:
            raise ValueError(
                f"Frame size {self.width}x{self.height} exceeds max allowed {MAX_FRAME_SIZE}"
            )

    def _isDarkFrame(
        self, frame: np.ndarray[Any, np.dtype[np.integer[Any] | np.floating[Any]]]
    ) -> bool:
        """Determine dark frames in an image, which is useful for filtering out."""

        # convert to gray scale for computation
        gray: np.ndarray[Any, np.dtype[np.integer[Any] | np.floating[Any]]] = (
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        )
        return np.average(gray) < self.darkframe_perc

    def create_video(self):
        """Creates a video uses multiple images frames."""
        import time

        start_time = time.time()
        video = cv2.VideoWriter(
            self.video_name,
            cv2.VideoWriter_fourcc(*"mp4v"),  # ty:ignore[unresolved-attribute]
            self.fps,
            (self.width, self.height),
        )
        try:
            for path in tqdm(
                self.image_paths, desc="🎥 Processing frames", unit="frame"
            ):
                if time.time() - start_time > PROCESSING_TIMEOUT:
                    raise TimeoutError("Video processing exceeded timeout limit")
                frame = cv2.imread(path)

                # skip unreadable files
                if frame is None:
                    continue

                # filter out dark frames
                if not self._isDarkFrame(frame):
                    video.write(frame)
        finally:
            # ensure resources are always released
            cv2.destroyAllWindows()
            video.release()
