import os
import shutil

module_path = os.path.abspath(__file__)
module_dir = os.path.dirname(module_path)

def create(day_num):
    src_dir = os.path.join(module_dir, '0')
    dest_dir = os.path.join(module_dir, str(day_num))
    src_files = os.listdir(src_dir)
    if os.path.exists(dest_dir):
        dest_files = os.listdir(dest_dir)
        if dest_files:
            raise Exception(f"destination {dest_dir} already exists and contains files: {dest_files}")
    else:
        os.makedirs(dest_dir)
    try:
        for sf in src_files:
            if '0' in sf:
                df = sf.replace('0', str(day_num))
            else:
                df = sf
            df = os.path.join(dest_dir, df)
            if os.path.exists(df):
                print(f"{df} already exists, skipping")
            else:
                print(f"copy {sf} to {df}")
                shutil.copy(os.path.join(src_dir, sf), df)
    except Exception as e:
        print(f"Error: {e}")
    print("done.")

def main():
    days = list(int(d) for d in os.listdir(module_dir) if d.isnumeric())
    max_day_num = max(days)
    print(f"{max_day_num=}")
    user_input = input("create next? [Y/n] ")
    if not len(user_input) or user_input.upper() == "Y":
        create(max_day_num + 1)

if __name__ == "__main__":
    main()