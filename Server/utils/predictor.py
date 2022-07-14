import re
import os
import numpy as np
import os.path as osp
import paddlers as pdrs
from PIL import Image


WORK_PATH = '/home/ubuntu/PaddleEarth'
MODEL_PATH = osp.join(WORK_PATH, 'models')
CACHE_PATH = osp.join(WORK_PATH, 'cache')
CD_MODEL_PATH = osp.join(MODEL_PATH, 'change_detection')
TD_MODEL_PATH = osp.join(MODEL_PATH, 'target_detection')
TE_MODEL_PATH = osp.join(MODEL_PATH, 'target_extraction')
TC_MODEL_PATH = osp.join(MODEL_PATH, 'terrain_classification')


class Predictor:


    def __init__(self,
                 cd_model_path,
                 td_model_path,
                 te_model_path,
                 tc_model_path,
                 patches_path):
        self.__patches_path = patches_path
        self.__images = []
        self.__images_name = []
        # self.__images_path = []
        self.__mode = None
        self.__in_size = None
        self.__pp_size = None
        self.__cpu_thread_num = 2
        # self.__crop_step = 512
        self.__cd_predictor = pdrs.deploy.Predictor(cd_model_path, cpu_thread_num=self.__cpu_thread_num)
        self.__td_predictor = pdrs.deploy.Predictor(td_model_path, cpu_thread_num=self.__cpu_thread_num)
        self.__te_predictor = pdrs.deploy.Predictor(te_model_path, cpu_thread_num=self.__cpu_thread_num)
        self.__tc_predictor = pdrs.deploy.Predictor(tc_model_path, cpu_thread_num=self.__cpu_thread_num)


    def __patches_generater(self, image, image_name, crop_size, crop_step):
        index_x, index_y, cur_width, cur_height = 0, 0, 0, 0
        crop_width, crop_height = crop_size
        pp_width, pp_height = self.__pp_size
        while cur_height + crop_height < pp_height + crop_step:
            index_x, cur_width = 0, 0
            while cur_width + crop_width < pp_width + crop_step:
                cur_image = Image.new(
                    mode='RGB',
                    size=(crop_width, crop_height),
                    color=(0, 0, 0)
                )
                cur_image.paste(
                    im=image.crop(box=(
                        cur_width,
                        cur_height,
                        cur_width + crop_width,
                        cur_height + crop_height
                    )),
                    box=(0, 0)
                )
                cur_image_path = osp.join(
                    self.__patches_path,
                    'patch_{}_{}_'.format(index_x, index_y) +
                    image_name
                )
                cur_image.save(cur_image_path)
                yield cur_image_path
                cur_width += crop_step
                index_x += 1
            cur_height += crop_step
            index_y += 1


    def __seam_patches(self, image_name, crop_step):
        image = Image.new(
            mode='RGB',
            size=self.__pp_size,
            color=(0, 0, 0)
        )
        for path in os.listdir(self.__patches_path):
            if re.search(image_name, path) is not None:
                patch_image = Image.open(osp.join(self.__patches_path, path))
                sp_items = path.split('_')
                index_x = int(sp_items[1])
                index_y = int(sp_items[2])
                # print('DEBUG', index_x, index_y, path)
                image.paste(
                    im=patch_image,
                    box=(index_x * crop_step, index_y * crop_step)
                )
        return image
    

    def __change_detect_single(self, images_path, output_path):
        result = self.__cd_predictor.predict(img_file=tuple(images_path))
        np_array = np.array(result[0]['label_map'])
        np_array = (np_array * 255).astype('uint8')
        result_image = Image.fromarray(np_array)
        result_image.save(output_path)


    def __change_detect(self, images_path, output_path):
        self.__images_preprocess(images_path, (1024, 1024))
        crop_step = 512
        patches_generaters = [
            self.__patches_generater(
                image=self.__images[i],
                image_name=self.__images_name[i],
                crop_size=(1024, 1024),
                crop_step=crop_step
            ) for i in range(2)
        ]
        while True:
            try:
                input_patches_path = [next(patches_generaters[i]) for i in range(2)]
                print('\n\n------------------ Inference Processing ---------------------')
                output_patch_path = osp.join(
                    osp.dirname(input_patches_path[0]),
                    osp.basename(input_patches_path[0]).split('.')[0] + '_result.png'
                )
                print(output_patch_path)
                self.__change_detect_single(
                    images_path=tuple(input_patches_path),
                    output_path=output_patch_path
                )
            except StopIteration:
                break
        output_image = self.__seam_patches(
            self.__images_name[0].split('.')[0] + '_result.png',
            crop_step
        )
        self.__images_postprocess(output_image).save(output_path)


    def __images_preprocess(self, images_path, model_input_shape):
        if self.__mode == 'change_detection':
            if type(images_path) is not tuple or len(images_path) != 2:
                raise Exception('Images paths should be tuple[str, str] in change detection mode.')
            self.__images_path = list(images_path)
            self.__images_name = [osp.basename(images_path[i]) for i in range(2)]
            self.__images = [Image.open(image_path) for image_path in images_path]
            if self.__images[0].size != self.__images[0].size:
                raise Exception('The size of two images should be same.')
        elif type(images_path) is not str:
            raise Exception('Images paths should be str.')
        else:
            self.__images_path = [images_path]
            self.__images_name = [osp.basename(images_path)]
            self.__images = [Image.open(images_path)]
            if self.__images[0].mode != 'RGB':
                self.__images[0] = self.__images[0].convert('RGB')
        self.__in_size = self.__images[0].size
        self.__pp_size = (
            max(self.__in_size[0], model_input_shape[0]),
            max(self.__in_size[1], model_input_shape[1])
        )
        for i in range(len(self.__images)):
            if self.__images[i].mode != 'RGB':
                self.__images[i] = self.__images[i].convert('RGB')
            if self.__images[i].size != self.__pp_size:
                image = Image.new(
                    mode='RGB',
                    size=self.__pp_size,
                    color=(0, 0, 0)
                )
                image.paste(
                    im=self.__images[i],
                    box=(0, 0)
                )
                self.__images[i] = image


    def __target_detect(self, image_path, output_path):
        image = Image.open(image_path)
        width, height = image.size
        if width != height:
            width = max(width, height, 608)
            height = max(width, height, 608)
            new_image = Image.new(mode=image.mode, size=(width, height), color=(0, 0, 0))
            new_image.paste(image, box=(0, 0))
            image = new_image
        scale_ratio = 1
        if width != 608:
            image = image.resize((608, 608), Image.BILINEAR)
            scale_ratio = 608 / width
        image_temp_path = osp.join(CACHE_PATH, osp.basename(image_path))
        image.save(image_temp_path)
        results = self.__td_predictor.predict(img_file=image_temp_path)
        for i in range(len(results)):
            for j in range(4):
                results[i]['bbox'][j] = round(results[i]['bbox'][j] / scale_ratio)
            results[i]['bbox'][2] += results[i]['bbox'][0]
            results[i]['bbox'][3] += results[i]['bbox'][1]
        return results


    def __target_extract_single(self, image_path, output_path):
        result = self.__te_predictor.predict(img_file=image_path)
        np_array = np.array(result['label_map'])
        np_array = (np_array * 255).astype('uint8')
        result_image = Image.fromarray(np_array)
        result_image.save(output_path)


    def __target_extract(self, images_path, output_path):
        self.__images_preprocess(images_path, (1500, 1500))
        crop_step = 750
        patches_generater = self.__patches_generater(
            image=self.__images[0],
            image_name=self.__images_name[0],
            crop_size=(1500, 1500),
            crop_step=crop_step
        )
        while True:
            try:
                input_patch_path = next(patches_generater)
                print('\n\n------------------ Inference Processing ---------------------')
                output_patch_path = osp.join(
                    osp.dirname(input_patch_path),
                    osp.basename(input_patch_path).split('.')[0] + '_result.png'
                )
                print(output_patch_path)
                self.__target_extract_single(
                    image_path=input_patch_path,
                    output_path=output_patch_path
                )
            except StopIteration:
                break
        output_image = self.__seam_patches(
            self.__images_name[0].split('.')[0] + '_result.png',
            crop_step
        )
        self.__images_postprocess(output_image).save(output_path)


    def __terrian_classify_single(self, image_path, output_path):
        result = self.__tc_predictor.predict(img_file=image_path)
        np_array = np.array(result['label_map'])
        result_image = Image.fromarray(np_array.astype('uint8'))
        result_image.save(output_path)

    
    def __terrian_classify(self, images_path, output_path):
        self.__images_preprocess(images_path, (256, 256))
        crop_step = 128
        patches_generater = self.__patches_generater(
            image=self.__images[0],
            image_name=self.__images_name[0],
            crop_size=(256, 256),
            crop_step=crop_step
        )
        while True:
            try:
                input_patch_path = next(patches_generater)
                print('\n\n------------------ Inference Processing ---------------------')
                output_patch_path = osp.join(
                    osp.dirname(input_patch_path),
                    osp.basename(input_patch_path).split('.')[0] + '_result.png'
                )
                print(output_patch_path)
                self.__terrian_classify_single(
                    image_path=input_patch_path,
                    output_path=output_patch_path
                )
            except StopIteration:
                break
        output_image = self.__seam_patches(
            self.__images_name[0].split('.')[0] + '_result.png',
            crop_step
        )
        self.__images_postprocess(output_image).save(output_path)


    def __images_postprocess(self, image):
        if image.size[0] > self.__in_size[0] or image.size[1] > self.__in_size[1]:
            image = image.crop(box=(0, 0, self.__in_size[0], self.__in_size[1]))
        return image


    def predict(self, images_path, output_path, mode):
        self.__mode = mode
        if self.__mode == 'change_detection':
            self.__change_detect(images_path, output_path)
            return None
        if self.__mode == 'target_detection':
            result = self.__target_detect(images_path, output_path)
            return result
        if self.__mode == 'target_extraction':
            self.__target_extract(images_path, output_path)
            return None
        if self.__mode == 'terrian_classification':
            self.__terrian_classify(images_path, output_path)
            return None
        raise Exception('No such predict mode.')


predictor = Predictor(
    cd_model_path=CD_MODEL_PATH,
    td_model_path=TD_MODEL_PATH,
    te_model_path=TE_MODEL_PATH,
    tc_model_path=TC_MODEL_PATH,
    patches_path=CACHE_PATH
)


# predictor.predict(
#     images_path='/home/ubuntu/PaddleEarth/static/images/tc_9780.jpg',
#     output_path='/home/ubuntu/PaddleEarth/static/images/result_tc_9780.jpg',
#     mode='terrian_classification'
# )
