import numpy as np
import tensorflow as tf
import cv2 as cv
from os import path
from tensorflow.keras.preprocessing import image
import os
import matplotlib.pyplot as plt

while True:
    try:
        new_model = tf.keras.models.load_model("./saved_model/model_2")
        break

    except:
        print(
            "error finding saved model. please ensure model is in the same file location in /saved_model/ for new use under name 'model_2'.")
        a = input("please enter model path of put exit to end program: ")
        if a == "exit" or a == "Exit":
            exit()
        else:
            new_model = tf.keras.models.load_model(a)
            break


def changeImage(directory, show=False, dim=(244, 244),
                localizes=True):  # Change images to selected size and grey scale.
    window_name = "Image"

    name = os.path.basename(os.path.normpath(directory))
    currectDic = os.getcwd()

    if not path.exists(currectDic + "/run_images"):
        os.mkdir(currectDic + "/run_images")

    if not path.exists(directory):
        raise Exception("cvImageChanger: findImage: no file exist, check location")

    item = cv.imread(
        directory)  # finds image, currently using test image replace original = cv.LoadImageM("image.jpg")

    resized = cv.resize(item, dim,
                        interpolation=cv.INTER_AREA)  # replace thumbnail = cv.CreateMat(original.rows/ 10, original.cols / 10, original.type) cv.Resize(original, thumbnail)

    if show:
        print("press ESC to exit")
        cv.imshow(window_name, item)  # shows image ?remove or make command based
        i = cv.waitKey(0)
        if (i == "ESC"):
            cv.destroyAllWindows()

    grey_image = cv.cvtColor(resized, cv.COLOR_RGB2GRAY)  # changes to grey

    if show:
        print("press ESC to exit")
        cv.imshow(window_name, grey_image)  # shows image ?remove or make command based
        i = cv.waitKey(0)
        if (i == "ESC"):
            cv.destroyAllWindows()

    if localizes:
        item = Localize(grey_image)

    if show:
        print("press ESC to exit")
        cv.imshow(window_name, item)  # shows image ?remove or make command based
        i = cv.waitKey(0)
        if (i == "ESC"):
            cv.destroyAllWindows()

        print(name)

    cv.imwrite(currectDic + "/run_images" + "/" + name, item)
    return (currectDic + "/run_images"), name


def Localize(img):
    ret2, item = cv.threshold(img, 0, 255,
                              cv.THRESH_BINARY + cv.THRESH_OTSU)  # cvThreshold(image, binary_image,128,255,CV_THRESH_OTSU)

    return item


def prepare_image(currectDic, name):
    if not path.exists("./run_images"):
        raise Exception("prep_image: findImage: no file exist, check location")

    img = image.load_img(currectDic + "/" + name, target_size=(224, 224))
    # img = PIL.Image.open(currectDic + "/" + name, (224, 224))
    # print(img)
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)


def guess():
    signs = ["30 mph", "50 mph", "60 mph", "70 mph", "junction", "Warning (empty)", "no entry",
             "Warning (!)"]  # correct names?

    LOC = input("please input full address of image: ")
    show = input("show image? True/False ")
    show.capitalize()
    if len(show) == 4:
        bool(show)
        currectDic, name = changeImage(LOC, show)  # C:\Users\gamin\OneDrive\Desktop\final project\1116055.jpg
    else:
        currectDic, name = changeImage(LOC)
    tool = prepare_image(currectDic, name)

    predictions_single = new_model.predict(tool)
    # print(predictions_single)

    for i in signs:
        if np.argmax(predictions_single) == signs.index(i):
            print("this sign is: ", np.argmax(predictions_single), ". Also know as: ", i)


def summ():
    new_model.summary()


def layers():
    print("total layers: " + str(len(new_model.layers) - 3))
    a = input("input first layer: ")
    if int(a) < 2:
        print("too low, changed to 2")
        a = "2"
    b = input("to layer: ")
    if int(b) > len(new_model.layers) - 3:
        print("too high changed to " + str(len(new_model.layers) - 3))
        b = str(len(new_model.layers) - 3)
    if (int(a) - int(b)) != 0:
        print("notice: layers done backwards")

    LOC = input("please input full address of image: ")
    show = input("show image? True/False ")
    for i in reversed(range(int(a), int(b) + 1)):
        print("layer - " + str(i))

        model_cut = tf.keras.Model(inputs=new_model.inputs, outputs=new_model.layers[i].output)
        if len(show) == 4:
            bool(show)
            currectDic, name = changeImage(LOC, show)
        else:
            currectDic, name = changeImage(LOC)
        img = prepare_image(currectDic, name)

        nodeImages = model_cut.predict(img)

        amountSize = nodeImages.shape[3]
        if amountSize > 100:
            user = input("amount of images over 64. recommend a sample instead. press Y for a smaller sample.")
            user.lower()
            if user == "y":
                amountSize = 64
                print("smaller size chosen")
            else:
                print("layering of plot will be done. warning lag may happen due to lots of images. ")

        size0 = amountSize // 7
        size = amountSize % 7
        layer = 1

        fig = plt.figure(figsize=(10, 7))
        for images in range(0, amountSize):
            fig.add_subplot((size0 + size), 7, images + 1)
            plt.imshow(nodeImages[0, :, :, layer - 1])
            plt.axis('off')
            #plt.title("MapFilter = " + str(i) + "." + str(layer))
            layer += 1

        print("image of layer: " + str(i))
        plt.show()

    print("finished")


def main():
    while True:
        print("")
        selection = input("please select 'guess' to input an image and guess which sign it is,"
                          " 'layer' to pick a image and see how each layer breaks it down, "
                          "'summary' to see total model summary or 'Exit' to end program: ")
        selection.lower()
        if selection == "guess" or selection == "g":
            guess()
        elif selection == "layer" or selection == "l":
            layers()
        elif selection == "summary" or selection == "s":
            summ()
        elif selection == "exit" or selection == "e":
            break
        else:
            print("error, option not selected. try again.")
            print("")

    quit()


if __name__ == "__main__":
    main()
