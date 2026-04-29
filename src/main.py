import os
from pathlib import Path
import sys

import click
from .video import TimelapseTool


@click.command()
@click.argument(
    "image_dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    required=True,
)
@click.option(
    "-o",
    "--output",
    type=click.Path(path_type=Path),
    default="timelapse.mp4",
    help="Output video filename. Defaults to 'timelapse.mp4'",
)
@click.option(
    "-f",
    "--fps",
    type=int,
    default=10,
    help="Frames per second for the video. Defaults to 10.",
)
@click.option(
    "-d",
    "--darkframe-perc",
    type=int,
    default=20,
    help="Dark frame threshold percentage. Frames with average brightness below this are filtered. Defaults to 20.",
)
def main(image_dir: Path, output: Path, fps: int, darkframe_perc: int):
    """Create a timelapse video from a directory of images.

    IMAGE_DIR is the path to the directory containing your images.
    """
    click.echo(f"🎬 Creating timelapse video from images in: {image_dir}")

    # Get all image files from the directory
    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}
    image_paths = [
        p
        for p in image_dir.iterdir()
        if p.is_file() and p.suffix.lower() in image_extensions
    ]

    if not image_paths:
        click.echo(
            f"❌ Error: No valid image files found in {image_dir}",
            err=True,
        )
        sys.exit(1)

    click.echo(f"📸 Found {len(image_paths)} images")

    try:
        tool = TimelapseTool(
            image_paths, output, fps=fps, darkframe_perc=darkframe_perc
        )
        click.echo(f"🔧 Video dimensions: {tool.width}x{tool.height}")
        click.echo(f"⚙️  FPS: {fps}, Dark frame threshold: {darkframe_perc}%")

        tool.create_video()

        click.echo(f"✅ Video created successfully: {output}")
        click.echo(f"📊 Video size: {os.path.getsize(output) / (1024*1024):.2f} MB")

    except ValueError as e:
        click.echo(f"❌ Error: {e}", err=True)
        sys.exit(1)
    except TimeoutError as e:
        click.echo(f"❌ Timeout: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
