import os
import hashlib
import numpy as np
import os.path as osp

from utils import analyse
from utils.predictor import Predictor
# import analyse
# from predictor import Predictor
from datetime import datetime
from PIL import Image, ImageDraw


WORK_PATH = '/home/ubuntu/PaddleEarth'
IMAGES_PATH = '/home/ubuntu/PaddleEarth/static/images'
MODEL_PATH = osp.join(WORK_PATH, 'models')
CACHE_PATH = osp.join(WORK_PATH, 'cache')
CD_MODEL_PATH = osp.join(MODEL_PATH, 'change_detection')
TD_MODEL_PATH = osp.join(MODEL_PATH, 'target_detection')
TE_MODEL_PATH = osp.join(MODEL_PATH, 'target_extraction')
TC_MODEL_PATH = osp.join(MODEL_PATH, 'terrain_classification')


predictor = Predictor(
    cd_model_path=CD_MODEL_PATH,
    td_model_path=TD_MODEL_PATH,
    te_model_path=TE_MODEL_PATH,
    tc_model_path=TC_MODEL_PATH,
    patches_path=CACHE_PATH
)


def change_detect(image1_url, image2_url, coordinates):
    clear_cache()
    images_path = [url_to_path(image1_url), url_to_path(image2_url)]
    images = [Image.open(path) for path in images_path]
    if (images[0].size != images[1].size):
        raise Exception('Change_detection: The two pictures are not the same size.')
    center_x = images[0].size[0] / 2
    center_y = images[0].size[1] / 2
    print('Before: ', coordinates)
    if len(coordinates) == 0:
        w, h = images[0].size
        coordinates = [(0, 0), (w, 0), (w, h), (0, h)]
    else:
        coordinates = [(int(x + center_x), int(center_y - y)) for x, y in coordinates]
    print('After: ', coordinates)
    predict_result_path = path_insert_prefix(
        path=osp.join(CACHE_PATH, osp.basename(images_path[0])),
        prefix='d_'
    )
    predictor.predict(
        images_path=tuple(images_path),
        output_path=predict_result_path,
        mode='change_detection'
    )
    result_image = Image.open(predict_result_path)
    image_mask = Image.new('L', images[0].size, 0)
    ImageDraw.Draw(image_mask).polygon(coordinates, outline=255, fill=255)
    black_image = Image.new('RGB', images[0].size, (0, 0, 0))
    result_image = Image.composite(result_image, black_image, image_mask)
    result_image_array = np.array(result_image.convert('1'))
    original_image_array = np.array(images[0].convert('RGB'))
    image_mask_array = np.array(image_mask)
    mask_count, result_count = 0, 0
    for x in range(original_image_array.shape[0]):
        for y in range(original_image_array.shape[1]):
            if result_image_array[x][y] == 1:
                original_image_array[x][y][0] = 255 # R
                original_image_array[x][y][1] = 0   # G
                original_image_array[x][y][2] = 0   # B
                result_count += 1
            if image_mask_array[x][y] != 0:
                mask_count += 1
    change_rate = result_count / mask_count
    result_image = Image.fromarray(original_image_array)
    result_image_path = filepath_encryption(
        filepath=path_insert_prefix(images_path[0], 'result_')
    )
    result_image.save(result_image_path)
    crop_box = get_box(coordinates)
    cover_rate = []
    box_width = crop_box[2] - crop_box[0]
    box_height = crop_box[3] - crop_box[1]
    x_step = box_width // 4
    y_step = box_height // 4
    box_pixel = x_step * y_step
    for row in range(4):
        for col in range(4):
            start_x = crop_box[0] + col * x_step
            start_y = crop_box[1] + row * y_step
            count = 0
            flag = False
            for x in range(start_x, start_x + x_step):
                for y in range(start_y, start_y + y_step):
                    if result_image_array[y][x] == 1:
                        count += 1
                    if image_mask_array[y][x] != 0:
                        flag = True
            if flag:
                cover_rate.append(count / box_pixel)
    print(cover_rate)
    scope, strength = analyse.changeDectionAnalyse(l=cover_rate)
    early_coverage, later_coverage = analyse.getBeforeAndAfter(change_rate)
    result = {
        'change': change_rate,
        'early_coverage': early_coverage,
        'later_coverage': later_coverage,
        'image_path': result_image_path,
        'scope': scope,
        'strength': strength
    }
    print('Interpreter:', result)
    return result


def target_detect(image_url, coordinates):
    clear_cache()
    image_path = url_to_path(image_url)
    image = Image.open(image_path)
    center_x = image.size[0] / 2
    center_y = image.size[1] / 2
    if len(coordinates) == 0:
        w, h = image.size
        coordinates = [(0, 0), (w, 0), (w, h), (0, h)]
    else:
        coordinates = [(int(x + center_x), int(center_y - y)) for x, y in coordinates]
    image_mask = Image.new('L', image.size, 0)
    ImageDraw.Draw(image_mask).polygon(coordinates, outline=255, fill=255)
    black_image = Image.new('RGB', image.size, (0, 0, 0))
    masked_image = Image.composite(image, black_image, image_mask)
    masked_image_path = path_insert_prefix(
        path=osp.join(CACHE_PATH, osp.basename(image_path)),
        prefix='masked_'
    )
    masked_image.save(masked_image_path)
    result_path = filepath_encryption(
        filepath=path_insert_prefix(image_path, 'result_')
    )
    results = predictor.predict(
        images_path=masked_image_path,
        output_path=None,
        mode='target_detection'
    )
    image_draw = ImageDraw.Draw(image)
    black_image_draw = ImageDraw.Draw(black_image)
    result_count = 0
    for result in results:
        if result['score'] < 0.5:
            continue
        result_count += 1
        x1, y1, x2, y2 = result['bbox']
        for i in range(5):
            points = [(x1 + i, y1 + i), (x1 + i, y2 - i), (x2 - i, y2 - i), (x2 - i, y1 + i)]
            image_draw.polygon(points, outline=(124, 255, 178), fill=None)
            black_image_draw.polygon(points, outline=(255, 255, 255), fill=(255, 255, 255))
    image.save(result_path)
    crop_box = get_box(coordinates)
    cover_rate = []
    box_width = crop_box[2] - crop_box[0]
    box_height = crop_box[3] - crop_box[1]
    x_step = box_width // 4
    y_step = box_height // 4
    box_pixel = x_step * y_step
    black_image_array = np.array(black_image.convert('1'))
    for row in range(4):
        for col in range(4):
            start_x = crop_box[0] + col * x_step
            start_y = crop_box[1] + row * y_step
            count = 0
            for x in range(start_x, start_x + x_step):
                for y in range(start_y, start_y + y_step):
                    if black_image_array[y][x] == 1:
                        count += 1
            cover_rate.append(count / box_pixel)
    # print(cover_rate)
    amount_score, scope_score, density_score, rationality = analyse.objectDectionAnalyse(cover_rate)
    result = {
        'image_path': result_path,
        'name': 'playground',
        'amount': result_count,
        'amount_score': amount_score,
        'scope_score': scope_score,
        'density_score': density_score,
        'rationality': rationality
    }
    print('Interpreter:', result)
    return result


def target_extract(image_url, coordinates):
    clear_cache()
    image_path = url_to_path(image_url)
    image = Image.open(image_path)
    center_x = image.size[0] / 2
    center_y = image.size[1] / 2
    if len(coordinates) == 0:
        w, h = image.size
        coordinates = [(0, 0), (w, 0), (w, h), (0, h)]
    else:
        coordinates = [(int(x + center_x), int(center_y - y)) for x, y in coordinates]
    predict_result_path = path_insert_prefix(
        path=osp.join(CACHE_PATH, osp.basename(image_path)),
        prefix='d_'
    )
    predictor.predict(
        images_path=image_path,
        output_path=predict_result_path,
        mode='target_extraction'
    )
    result_image = Image.open(predict_result_path)
    image_mask = Image.new('L', image.size, 0)
    ImageDraw.Draw(image_mask).polygon(coordinates, outline=255, fill=255)
    black_image = Image.new('RGB', image.size, (0, 0, 0))
    result_image = Image.composite(result_image, black_image, image_mask)
    result_image_array = np.array(result_image.convert('1'))
    original_image_array = np.array(image)
    image_mask_array = np.array(image_mask)
    mask_count, result_count = 0, 0
    for x in range(original_image_array.shape[0]):
        for y in range(original_image_array.shape[1]):
            if result_image_array[x][y] == 1:
                original_image_array[x][y][0] = 255 # R
                original_image_array[x][y][1] = 0   # G
                original_image_array[x][y][2] = 0   # B
                result_count += 1
            if image_mask_array[x][y] != 0:
                mask_count += 1
    coverage = result_count / mask_count
    result_image = Image.fromarray(original_image_array)
    result_image_path = filepath_encryption(
        filepath=path_insert_prefix(image_path, 'result_')
    )
    result_image.save(result_image_path)
    crop_box = get_box(coordinates)
    cover_rate = []
    box_width = crop_box[2] - crop_box[0]
    box_height = crop_box[3] - crop_box[1]
    x_step = box_width // 4
    y_step = box_height // 4
    box_pixel = x_step * y_step
    for row in range(4):
        for col in range(4):
            start_x = crop_box[0] + col * x_step
            start_y = crop_box[1] + row * y_step
            count = 0
            flag = False;
            for x in range(start_x, start_x + x_step):
                for y in range(start_y, start_y + y_step):
                    if result_image_array[y][x] != 0:
                        count += 1
                    if image_mask_array[y][x] != 0:
                        flag = True
            if flag:
                cover_rate.append(count / box_pixel)
    print(cover_rate)
    cover_score, scale_score, accessible_score, matching_score, totality_level = analyse.objectExtractionAnalyse(
        l=cover_rate
    )
    result = {
        'image_path': result_image_path,
        'coverage' : coverage,
        'cover_score': cover_score,
        'scale_score': scale_score,
        'accessible_score': accessible_score,
        'matching_score': matching_score,
        'totality_level': totality_level
    }
    print('Interpreter:', result)
    return result


def terrian_classify(image_url, coordinates):
    clear_cache()
    image_path = url_to_path(image_url)
    image = Image.open(image_path)
    center_x = image.size[0] / 2
    center_y = image.size[1] / 2
    if len(coordinates) == 0:
        w, h = image.size
        coordinates = [(0, 0), (w, 0), (w, h), (0, h)]
    else:
        coordinates = [(int(x + center_x), int(center_y - y)) for x, y in coordinates]
    predict_result_path = path_insert_prefix(
        path=osp.join(CACHE_PATH, osp.basename(image_path)),
        prefix='d_'
    )
    predictor.predict(
        images_path=image_path,
        output_path=predict_result_path,
        mode='terrian_classification'
    )
    result_image = Image.open(predict_result_path)
    image_mask = Image.new('L', image.size, 0)
    ImageDraw.Draw(image_mask).polygon(coordinates, outline=255, fill=255)
    black_image = Image.new('RGB', image.size, (0, 0, 0))
    result_image = Image.composite(result_image, black_image, image_mask)
    result_image_array = np.array(result_image.convert('L'))
    original_image_array = np.array(image)
    image_mask_array = np.array(image_mask)
    mask_count = 0
    count = [0] * 4
    for x in range(original_image_array.shape[0]):
        for y in range(original_image_array.shape[1]):
            if image_mask_array[x][y] == 0:
                continue
            mask_count += 1
            if result_image_array[x][y] == 0:
                original_image_array[x][y][0] = 124 # R
                original_image_array[x][y][1] = 255 # G
                original_image_array[x][y][2] = 178 # B
                count[0] += 1
            elif result_image_array[x][y] == 1:
                original_image_array[x][y][0] = 253 # R
                original_image_array[x][y][1] = 221 # G
                original_image_array[x][y][2] = 96  # B
                count[1] += 1
            elif result_image_array[x][y] == 2:
                original_image_array[x][y][0] = 73  # R
                original_image_array[x][y][1] = 146 # G
                original_image_array[x][y][2] = 255 # B
                count[2] += 1
            elif result_image_array[x][y] == 3:
                original_image_array[x][y][0] = 255 # R
                original_image_array[x][y][1] = 110 # G
                original_image_array[x][y][2] = 118 # B
                count[3] += 1
    # coverage = result_count / mask_count
    coverage = [c / mask_count for c in count];
    result_image = Image.fromarray(original_image_array)
    result_image_path = filepath_encryption(
        filepath=path_insert_prefix(image_path, 'result_')
    )
    result_image.save(result_image_path)
    crop_box = get_box(coordinates)
    cover_rate = [[] for _ in range(3)]
    box_width = crop_box[2] - crop_box[0]
    box_height = crop_box[3] - crop_box[1]
    x_step = box_width // 4
    y_step = box_height // 4
    box_pixel = x_step * y_step
    for row in range(4):
        for col in range(4):
            start_x = crop_box[0] + col * x_step
            start_y = crop_box[1] + row * y_step
            count = [0, 0, 0]
            flag = False
            for x in range(start_x, start_x + x_step):
                for y in range(start_y, start_y + y_step):
                    if result_image_array[y][x] < 3:
                        count[result_image_array[y][x]] += 1
                    if image_mask_array[y][x] != 0:
                        flag = True
            if flag:
                for i in range(3):
                    cover_rate[i].append(count[i] / box_pixel)
    print(cover_rate)
    rationality, availabity = analyse.classifictionAnalyse(
        cover_rate[0],
        cover_rate[1],
        cover_rate[2]
    )
    # rationality, availabity = 'A', 'A'
    result = {
        'image_path': result_image_path,
        'building_coverage': coverage[0],
        'road_coverage': coverage[1],
        'forest_coverage': coverage[2],
        'rationality': rationality,
        'availability': availabity
    }
    print('Interpreter:', result)
    return result


def url_to_path(url):
    basename = osp.basename(url)
    return osp.join(IMAGES_PATH, basename)


def path_insert_prefix(path, prefix):
    return osp.join(osp.dirname(path), prefix + osp.basename(path))


def get_box(coordinates):
    x1 = 10 ** 10
    y1 = 10 ** 10
    x2 = -(10 ** 10)
    y2 = -(10 ** 10)
    for x, y in coordinates:
        x1 = min(x1, x)
        y1 = min(y1, y)
        x2 = max(x2, x)
        y2 = max(y2, y)
    return x1, y1, x2, y2


def filepath_encryption(filepath):
    filename = osp.basename(filepath)
    filepath = osp.dirname(filepath)
    current_time = datetime.now()
    time = datetime.strftime(current_time, '%Y-%m-%d %H:%M:%S')
    name_tuple = filename.rpartition('.')
    name = hashlib.md5((name_tuple[0] + time).encode(encoding='UTF-8')).hexdigest()
    filename = name + name_tuple[1] + name_tuple[2]
    return osp.join(filepath, filename)


def clear_cache():
    for path in os.listdir(CACHE_PATH):
        asb_path = osp.join(CACHE_PATH, path)
        if osp.isfile(asb_path):
            os.remove(asb_path)
        else:
            os.rmdir(asb_path)


# print(change_detect(
#     image1_url='http://127.0.0.1:80/static/images/CD_A.png',
#     image2_url='http://127.0.0.1:80/static/images/CD_B.png',
#     coordinates=[
#         # [50.12900000000002, -180.173],
#         # [325.82899999999995, 194.841],
#         # [470.8710000000001, -185.8707],
#         # [50.12900000000002, -180.173]
#     ]
# ))


# print(target_detect(
#     image_url='http://127.0.0.1:80/static/images/TD.jpg',
#     coordinates=[
#         # [-237.5, -261.5],
#         # [-237.5, 213.5],
#         # [262.5, 213.5],
#         # [262.5, -261.5],
#         # [-237.5, -261.5]
#     ]
# ))

# print(target_extract(
#     image_url='/home/ubuntu/PaddleEarth/static/images/TE.jpg',
#     coordinates=[
#         # [50.12900000000002, -180.173],
#         # [325.82899999999995, 194.841],
#         # [470.8710000000001, -185.8707],
#         # [50.12900000000002, -180.173]
#     ]
# ))


# print(terrian_classify(
#     image_url='http://127.0.0.1:80/static/images/5288.jpg',
#     coordinates=[
#         [-37.8, -82.877],
#         [-78, 13],
#         [91.9234, -106.77],
#         [-37.8, -82.877]
#     ]
# ))