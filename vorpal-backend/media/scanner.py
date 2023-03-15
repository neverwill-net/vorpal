import os
import concurrent.futures
#from cachetools import cached, TTLCache
from .metadata import get_metadata
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeRemainingColumn,
)

#cache = TTLCache(maxsize=1024, ttl=2592000)  # 1 month

#@cached(cache)
def scan_file(file_path, cache=None, debug=False):
    return get_metadata(file_path, debug=debug)

def scan_media_files(directory, cache=None, debug=False, num_threads=None):
    console = Console()
    media_files = []
    files = list(get_media_files(directory))
    total_files = len(files)
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        with Progress(
            TextColumn("[bold blue]{task.completed}/{task.total}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("[cyan]{task.fields[process]}"),
            TextColumn("[bold magenta]{task.fields[filename]}", justify="right"),
            console=console,
        ) as progress:
            task = progress.add_task(
                "Scanning media files...",
                total=total_files,
                process="Process 1",
                filename="",
            )
            futures = {executor.submit(scan_file, file_path, cache=cache, debug=debug): file_path for file_path in files}
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                try:
                    file_path = futures[future]
                    file_metadata = future.result()
                    if file_metadata:
                        media_files.append(file_metadata)
                except Exception as e:
                    console.print(f"[red]Failed to scan media file: {e}")
                    continue
                progress.update(
                    task,
                    advance=1,
                    filename=file_path,
                    completed=i + 1,
                    total=total_files,
                    process=f"Process {i % num_threads + 1}",
                )
            progress.remove_task(task)
    return media_files

def get_media_files(directory):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            files.append(os.path.join(root, filename))
    return files

