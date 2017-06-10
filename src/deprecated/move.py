import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc
from PIL import Image

DEBUG_3 = False

'''THIS FILE IS DEPRECATED USED FOR MOVING FILES AND RESIZING, CODE STILL USEFULL FOR COPYING'''

def main():
    for filename in os.listdir('data'):
        if 'Wrd_' in filename:
            directory = filename[0:12]
            if not os.path.exists('data/'+directory):
                os.makedirs('data/'+directory)
            os.rename('data/'+filename, 'data/'+directory+'/'+filename)
        else:
            directory = filename[0:4]
            if not os.path.exists('data/'+directory):
                os.makedirs('data/'+directory)
            os.rename('data/'+filename, 'data/'+directory+'/'+filename)

def count():
    txt = ''
    total = 0
    for dir in os.listdir('annotated_crops/128_extended'):
        txt = txt+dir
        count = 0
        pa = os.path.join('annotated_crops/128_extended', dir)
        print(len(os.listdir(pa)))
        for filename in os.listdir(pa):
            pat = os.path.join(pa, filename)
            if os.path.isfile(pat):
                count += 1
                total += 1
        txt = txt + ', ' + str(count) + '\n'
        
    print(total)
    text_file = open("Occurences_extended_once.txt", "w")
    text_file.write(txt)
    text_file.close()

def count_ones():
    count_one = 0
    count_total = 0
    for dir in os.listdir('../../data/Train/annotated_crops/128_extended_bin'):
        pa = os.path.join('../../data/Train/annotated_crops/128_extended_bin', dir)
        count_total += 1
        if len(os.listdir(pa))==1:
            count_one +=1
    print(count_total, count_one, count_one/count_total*100)

def sizes():
    orig = 'annotated_crops/original'
    new = 'annotated_crops/128'
    sizes = np.zeros((27025,2), dtype=int)
    i=0
    for dir in os.listdir(orig):
        if not os.path.exists('annotated_crops/128/'+dir):
           os.makedirs('annotated_crops/128/'+dir)
        pa = os.path.join(orig, dir)
        pa2 = os.path.join(new, dir)
        for filename in os.listdir(pa):
            pat = os.path.join(pa, filename)
            if os.path.isfile(pat):
                image = misc.imread(pat)
                image = image.astype(int)
                sizes[i] = [image.shape[0], image.shape[1]]
                i += 1

                if image.shape[0]!=image.shape[1]:

                    if image.shape[0] >= image.shape[1]:
                        max_size = image.shape[0]
                    else:
                        max_size = image.shape[1]

                    if DEBUG_3:
                        fig = plt.figure()
                        fig.add_subplot(3, 1, 1)
                        plt.imshow(image, cmap=plt.cm.gray, vmin=0, vmax=1)

                    diff0 = (max_size - image.shape[0])
                    if diff0 <= 0:
                        pass
                    else:
                        if diff0%2!=0:
                            diff0 += 1
                            a = np.ones((1, image.shape[0]), dtype=np.int)
                            a = a * 255
                            image = np.insert(image, 0, a, 1)
                        diff0 = int(diff0/ 2)
                        a = np.ones((diff0, image.shape[1]), dtype=np.int)
                        a = a*255
                        image = np.insert(image, 0, a, 0)
                        image = np.concatenate((image, a), axis=0)

                    diff1 = max_size - image.shape[1]
                    if diff1 <= 0:
                        pass
                    else:
                        if diff1%2!=0:
                            diff1 += 1
                            a = np.ones((1, image.shape[1]), dtype=np.int)
                            a = a * 255
                            image = np.insert(image, 0, a, 0)
                        diff1 = int(diff1/ 2)
                        a = np.ones((diff1, image.shape[0]), dtype=np.int)
                        a = a*255
                        image = np.insert(image, 0, a, 1)
                        a = np.ones((image.shape[0], diff1), dtype=np.int)
                        a = a*255
                        image = np.concatenate((image, a), axis=1)

                    if DEBUG_3:
                        fig.add_subplot(3,1,2)
                        plt.imshow(image, cmap=plt.cm.gray, vmin=0, vmax=1)

                new_image = misc.imresize(image, (120,120), interp='nearest')
                a = np.ones((4, new_image.shape[0]), dtype=np.int)
                a = a * 255
                new_image = np.insert(new_image, 0, a, 1)
                a = np.ones((new_image.shape[0], 4), dtype=np.int)
                a = a * 255
                new_image = np.concatenate((new_image, a), axis=1)
                a = np.ones((4, new_image.shape[1]), dtype=np.int)
                a = a * 255
                new_image = np.insert(new_image, 0, a, 0)
                new_image = np.concatenate((new_image, a), axis=0)
                image = new_image

                if DEBUG_3:
                    fig.add_subplot(3,1,3)
                    plt.imshow(new_image, cmap=plt.cm.gray, vmin=0, vmax=1)
                    plt.show()

                im = Image.fromarray(image.astype(np.uint8))
                im.save(pa2 + '/' + filename)

    print('done')

if __name__ == '__main__':
    count_ones()

