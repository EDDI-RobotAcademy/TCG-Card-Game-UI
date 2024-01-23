import os


def get_project_root():
    current_directory = os.path.abspath(os.getcwd())

    while not os.path.exists(os.path.join(current_directory, 'TCG-Card-Game-UI')):
        # 부모 디렉토리로 이동
        current_directory = os.path.abspath(os.path.join(current_directory, os.pardir))

        # 루트 디렉토리에 도달한 경우
        if current_directory == os.path.abspath(os.sep):
            return None

    return os.path.join(current_directory, 'TCG-Card-Game-UI')

