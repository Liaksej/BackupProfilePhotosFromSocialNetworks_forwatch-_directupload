import requests
import os


class VkToYaDsk:
    def __init__(self, token: str):
        self.token = token

    def download_photo(self, file_path_to_save: str, owner_id: int):
        url = 'https://api.vk.com/method/photos.get'
        # headers = self.get_headers()
        params = {'owner_id': owner_id, 'album_id': 'profile', 'extended': 1, 'access_token': self.token, 'v': '5.131'}
        response = requests.get(url=url, params=params)
        photoalbums = response.json()
        album_best_resolution = []
        for y in photoalbums['response']['items']:
            # maximum_height_photo = max(y['sizes'], key=(lambda x: x['height']))
            maximum_height_photo = y['sizes'][-1]
            album_best_resolution.append(maximum_height_photo['url'])
        return album_best_resolution

    def save_photo(self, file_path_to_save, owner_id):
        listik = self.download_photo(file_path_to_save, owner_id)
        for x, y in enumerate(listik):
            reqs = requests.get(y)
            with open(file_path_to_save + '/' + f'{str(x)}.jpg', 'wb') as code:
                code.write(reqs.content)
        return 'Done'


class YaUploader(VkToYaDsk):

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def upload(self, disk_file_path: str, filelist):
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

if __name__ == '__main__':
    token_vk = 'vk1.a.kYn1IfCsd4Di9_f7a0vwj6fhdbLvVa9cFhg7W_EKaczjrTMK8PbY5NJqK4mVbCuo382b5-EEI1moN4Su2sJvyeg1GkV2zGPAP0x9p-PmiXH9jI28O51q4HVpqczwe52WLkikcVdE6-c1zUim5gPJU9okS6hw3DizzYeZgeNTxNefCMQ8NVXJY0AT8_7FU2dx'
    owner_id = 7451160
    file_path_to_save = 'Photos'
    downloader = VkToYaDsk(token_vk)
    downloader.save_photo(file_path_to_save, owner_id)

    token_yd = 'AQAAAAAirg3lAADLWyKCRKHJ4kpflbLSVeaV5Go'
    filelist = os.listdir('Photos')
    disk_file_path = 'Photos_VK'
    uploader = YaUploader(token_yd)
    result = uploader.upload(disk_file_path, filelist)
