import requests
import os
from datetime import datetime


class VkDownload:

    def __init__(self, token: str):
        self.token = token

    def download_photo(self, file_path_to_local_save: str, owner_id: int):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': owner_id, 'album_id': 'profile', 'extended': 1, 'access_token': self.token, 'v': '5.131'}
        response = requests.get(url=url, params=params)
        photoalbum = response.json()
        if not os.path.exists(file_path_to_local_save):
            os.mkdir(file_path_to_local_save)
            print('Успешно создана папка', file_path_to_local_save)
        control_naming_pattern = {}
        for y in photoalbum['response']['items']:
            file_name = f'{y["likes"]["count"]}.jpg'
            if file_name in control_naming_pattern:
                control_naming_pattern[file_name] += 1
            else:
                control_naming_pattern[file_name] = 1
        data_for_json = []
        for y in photoalbum['response']['items']:
            content_for_json_item = {}
            reqs = requests.get(y['sizes'][-1]['url'])
            if f'{y["likes"]["count"]}.jpg' in control_naming_pattern and\
                    control_naming_pattern[f'{y["likes"]["count"]}.jpg'] > 1:
                with open(file_path_to_local_save + '/' +
                          (f'{y["likes"]["count"]}_'
                           f'{datetime.utcfromtimestamp(int(y["date"])).strftime("%d.%m.%Y")}.jpg'),
                          'wb') as code:
                    code.write(reqs.content)
                content_for_json_item['file_name'] = \
                    f'{y["likes"]["count"]}_{datetime.utcfromtimestamp(int(y["date"])).strftime("%d.%m.%Y")}.jpg'
                content_for_json_item['size'] = f'{y["sizes"][-1]["height"]}x{y["sizes"][-1]["width"]}'
                data_for_json.append(content_for_json_item)
            else:
                with open(file_path_to_local_save + '/' + f'{y["likes"]["count"]}.jpg', 'wb') as code:
                    code.write(reqs.content)
                content_for_json_item['file_name'] = f'{y["likes"]["count"]}.jpg'
                content_for_json_item['size'] = f'{y["sizes"][-1]["height"]}x{y["sizes"][-1]["width"]}'
                data_for_json.append(content_for_json_item)
        with open(file_path_to_local_save + '/' + 'photo_data.json', 'w') as file:
            file.write(f'{data_for_json}')


class YaDiscUpload(VkDownload):

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def upload(self, disk_file_path: str, filelist: list):
        url_for_dir = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = self.get_headers()
        params_for_dir = {'path': disk_file_path}
        response_get_folder = requests.put(url=url_for_dir, headers=headers, params=params_for_dir)
        if response_get_folder.status_code == 201 or 409:
            for count, file in enumerate(filelist):
                url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
                params = {'path': disk_file_path + '/' + file, 'overwrite': 'true'}
                response_get_link = requests.get(url=url, headers=headers, params=params)
                request_for_url = response_get_link.json()
                url_for_upload = request_for_url.get('href', '')
                response_upload = requests.put(url_for_upload, data=open(f'Photos/{file}', 'rb'))
                response_upload.raise_for_status()
                if response_upload.status_code == 201:
                    print(f'{count + 1} файл из {len(filelist)} файлов с именем {file} загружен успешно')
        else:
            print('Ошибка соединения. Попробуйте еще раз или обратитесь к разработчнику.')


if __name__ == '__main__':
    token_vk = str(input('Введите токен VK: '))
    owner_id = int(input('Введите ваш id в VK: '))
    file_path_to_save = 'Photos'
    downloader = VkDownload(token_vk)
    downloader.download_photo(file_path_to_save, owner_id)

    token_yd = str(input('Введите токен YandexDisk: '))
    filelist = os.listdir('Photos')
    disk_file_path = 'Photos_VK'
    uploader = YaDiscUpload(token_yd)
    uploader.upload(disk_file_path, filelist)
