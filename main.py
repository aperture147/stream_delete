from db_helper import Database
import configparser
import os.path
from datetime import datetime, timedelta
from shutil import rmtree

config = configparser.ConfigParser()
config.read('config.ini')

db = Database(
    host=config['database']['host'],
    user=config['database']['username'],
    password=config['database']['password'],
    db_name=config['database']['database']
)


def content_delete(path, threshold):
    dir_list = os.listdir(path)
    del_dir_list = [
        os.path.join(path, dir_str)
        for dir_str in dir_list
        if int(dir_str) < threshold
    ]
    for del_dir in del_dir_list:
        rmtree(del_dir)
        print(f"deleted {del_dir}")


if __name__ == '__main__':
    days = db.get_daily_content_reserve_days()

    current_datetime = datetime.now() - timedelta(days=days)

    print(f"today: {str(datetime.now().date())}")
    print(f"deleting file older than {str(current_datetime.date())}")

    current_year = current_datetime.year
    current_month = current_datetime.month
    current_day = current_datetime.day

    current_year_str = str(current_year)
    current_month_str = f"{current_month:02d}"

    channels = db.get_all_channels()
    data_path = config['resource']['path']

    for channel in channels:
        delete_list = [
            (os.path.join(data_path, 'raw', channel), current_year),
            (os.path.join(data_path, 'output', channel), current_year),
            (os.path.join(data_path, 'raw', channel, current_year_str), current_month),
            (os.path.join(data_path, 'output', channel, current_year_str), current_month),
            (os.path.join(data_path, 'raw', channel, current_year_str, current_month_str), current_day),
            (os.path.join(data_path, 'output', channel, current_year_str, current_month_str), current_day),
        ]

        for delete_path, delete_threshold in delete_list:
            if os.path.exists(delete_path):
                print(f"selectively deleting files in {delete_path} with threshold {delete_threshold}")
                content_delete(delete_path, delete_threshold)
            else:
                print(f"delete path {delete_path} does not exist")
