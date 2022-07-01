import requests
import os
from pprint import pprint


class VkToYaDsk:

    def __init__(self, token: str):
        self.token = token

    def download_photo(self, file_path_to_save, owner_id: int):
        url = 'https://api.vk.com/method/photos.get'
        # headers = self.get_headers()
        params = {'owner_id': owner_id, 'album_id': 'profile', 'extended': 1, 'access_token': self.token, 'v': '5.131'}
        response = requests.get(url=url, params=params)
        photoalbum = response.json()
        if not os.path.exists(file_path_to_save):
            os.mkdir(file_path_to_save)
            print('Successfully created directory', file_path_to_save)
        album_best_resolution = []
        data_for_json = []
        content_for_json_item = {}
        for y in photoalbum['response']['items']:
            maximum_height_photo = y['sizes'][-1]
            album_best_resolution.append(maximum_height_photo['url'])
            content_for_json_item['file_name'] = (f'{y["likes"]["count"]}.jpg')
            content_for_json_item['size'] = (f'{y["sizes"][-1]["height"]}x{y["sizes"][-1]["width"]}.jpg')
            data_for_json.append(content_for_json_item)
            reqs = requests.get(y['sizes'][-1]['url'])
            with open(file_path_to_save + '/' + f'{y["likes"]["count"]}.jpg', 'wb') as code:
                code.write(reqs.content)
        with open(file_path_to_save + '/' + f'photo_data.json', 'w') as file:
            file.write(f'{data_for_json}')

        # counter_of_words_in_phrase = {}
        # for element in data_for_json:
        #     m = element['file_name']
        #     if m in counter_of_words_in_phrase:
        #         counter_of_words_in_phrase[m] += 1
        #     else:
        #         counter_of_words_in_phrase[m] = 1
        # for x counter_of_words_in_phrase.values():
        #     if x > 1:
        #         del counter_of_words_in_phrase[x]
        # for x in data_for_json:
        #     if x['file_name'] in counter_of_words_in_phrase.keys():
        #     x['file_name'] = (f'{y["likes"]["count"]} {}.jpg') + return album_best_resolution, data_for_json
        # pprint(photoalbum)

    # def save_photo(self, file_path_to_save):
    #     if not os.path.exists(file_path_to_save):
    #         os.mkdir(file_path_to_save)
    #         print('Successfully created directory', file_path_to_save)
    #     listik = self.download_photo(owner_id)
    #     for y in enumerate(listik[0]):
    #         reqs = requests.get(y)
    #         with open(file_path_to_save + '/' + f'{filestr(x)}.jpg', 'wb') as code:
    #             code.write(reqs.content)
        # return 'Done'


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
        else:
            print('Ошибка соединения. Попробуйте еще раз или обратитесь к разработчнику.')

if __name__ == '__main__':
    token_vk = 'vk1.a.kYn1IfCsd4Di9_f7a0vwj6fhdbLvVa9cFhg7W_EKaczjrTMK8PbY5NJqK4mVbCuo382b5-EEI1moN4Su2sJvyeg1GkV2zGPAP0x9p-PmiXH9jI28O51q4HVpqczwe52WLkikcVdE6-c1zUim5gPJU9okS6hw3DizzYeZgeNTxNefCMQ8NVXJY0AT8_7FU2dx'
    owner_id = 7451160
    file_path_to_save = 'Photos'
    downloader = VkToYaDsk(token_vk)
    # downloader.save_photo(file_path_to_save)
    downloader.download_photo(file_path_to_save, owner_id)

    # token_yd = 'AQAAAAAirg3lAADLWyKCRKHJ4kpflbLSVeaV5Go'
    # filelist = os.listdir('Photos')
    # disk_file_path = 'Photos_VK'
    # uploader = YaUploader(token_yd)
    # result = uploader.upload(disk_file_path, filelist)
