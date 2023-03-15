import os
import argparse
from media.models import MediaFile
from config.config import load_config
from media.database import create_database, get_session
from media.scanner import scan_media_files
def print_database_info(session):
    print(f"Number of items in database: {session.query(MediaFile).count()}")

    items = session.query(MediaFile).limit(10).all()
    for i, item in enumerate(items):

        print(f"\nItem {i + 1}/{len(items)}:")
        print(f"  unique_id: {item.unique_id}")
        print(f"  file_path: {item.file_path}")
        print(f"  file_size: {item.file_size}")
        print(f"  hash: {item.hash}")
        print(f"  duration: {item.duration}")
        print(f"  bit_rate: {item.bit_rate}")
        print(f"  sample_rate: {item.sample_rate}")
        print(f"  channels: {item.channels}")
        print(f"  format_name: {item.format_name}")
        print(f"  format_long_name: {item.format_long_name}")
        print(f"  media_metadata: {item.media_metadata}")  # Add this line to print media_metadata

def main():
    parser = argparse.ArgumentParser(description='Scan media files and display metadata.')
    parser.add_argument('--debug', action='store_true', help='enable debug mode')
    parser.add_argument('--print-database', action='store_true', help='print database info and exit')
    args = parser.parse_args()

    config = load_config()

    media_directory = config['media']['directory']
    if not os.path.isdir(media_directory):
        print(f"Media directory '{media_directory}' does not exist.")
        exit(1)

    create_database()

    if not args.print_database:
        try:
            media_files = scan_media_files(media_directory, debug=args.debug, num_threads=4)
        except KeyboardInterrupt:
            print("KeyboardInterrupt detected, gracefully shutting down...")
            return


        session = get_session()
        for new_media_file in media_files:
            existing_media_file = session.query(MediaFile).filter(MediaFile.file_path == new_media_file.file_path).one_or_none()

            if existing_media_file:
                attributes_to_check = [
                    "file_size",
                    "hash",
                    "duration",
                    "bit_rate",
                    "sample_rate",
                    "channels",
                    "format_name",
                    "format_long_name",
                ]

                update_needed = False
                for attr in attributes_to_check:
                    if getattr(existing_media_file, attr) != getattr(new_media_file, attr):
                        update_needed = True
                        setattr(existing_media_file, attr, getattr(new_media_file, attr))
                if update_needed:
                    #print(f"Updating media metadata for {existing_media_file.file_path}: {existing_media_file.media_metadata}")
                    session.add(existing_media_file)
                    session.commit()
            else:
                #print(f"Adding media metadata for {new_media_file.file_path}: {new_media_file.media_metadata}")
                session.add(new_media_file)
                session.commit()
    else:
        session = get_session()
        print_database_info(session)


if __name__ == '__main__':
    main()

