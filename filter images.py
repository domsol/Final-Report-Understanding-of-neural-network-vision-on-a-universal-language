from os import path
import os
import cv2 as cv



def files(directory, newDirectory, layer=0, one=False):
    if one:  # one image for system to change
        settings = [False, (244, 244), True]  # defaults settings
        print("current settings: directory = ", directory, "show=", settings[0], "dim=", settings[1], "localizes=",
              settings[2])
        i = input("change settings? (Y)")
        i = i.lower()
        if i == "y" or i == "yes":  # change settings for one image
            for x in range(len(settings)):
                print("type new input in same format as: ", settings[x])  # loop the different settings
                b = input()
                if type(settings[x]) is tuple:  # changes size of image

                    try:
                        eval(b)
                    except:
                        print("wrong input value or no value. !using default!")
                    else:
                        if len(eval(b)) == 2:
                            print("layout correct, changing values to", eval(b))
                            settings[x] = eval(b)
                        else:
                            print("wrong value size. !using default!")


                elif b.lower() == "true" or b.lower() == "false":  # chages show, and localizes settings
                    b.capitalize()
                    settings[x] = bool(b)
                    print("correct value, changing to:", b)

                else:
                    print("value input wrong or no input. !using default!")

            print("new settings: directory = ", directory, "show=", settings[0], "dim=", settings[1], "localizes=",
                  settings[2])
            print("running")
            q = changeImage(directory, settings[0], settings[1], settings[2])
            cv.imwrite(newDirectory, q)
        else:  # default settings for one image
            print("running default image ")
            a = changeImage(directory)
            cv.imwrite(newDirectory, a)
    else:
        settings = [False, (244, 244), True]
        print("current settings: directory = ", directory, "show=", settings[0], "dim=", settings[1], "localizes=",
              settings[2])
        i = input("change settings? (Y)")
        i = i.lower()
        if i == "y" or i == "yes":
            for x in range(len(settings)):
                print("type new input in same format as: ", settings[x])
                b = input()
                if type(settings[x]) is tuple:
                    if b is None:
                        pass
                    try:
                        eval(b)
                    except:
                        print("wrong input value or no value. !using default!")
                    else:
                        if len(eval(b)) == 2:
                            print("layout correct, changing values to", eval(b))
                            settings[x] = eval(b)
                        else:
                            print("wrong value size. !using default!")


                elif b.lower() == "true" or b.lower() == "false":
                    b.capitalize()
                    settings[x] = bool(b)
                    print("correct value, changing to:", b)

                else:
                    print("value input wrong or no input. !using default!")

            print("new settings: directory = ", directory, "show=", settings[0], "dim=", settings[1], "localizes=",
                  settings[2])
            print("running")

        filentitles = {}

        for file in os.listdir(directory):
            print(directory + "/" + file)
            filename = os.fsdecode(file)

            if os.path.isdir(directory + "/" + file):
                print("a", file)
                if directory == newDirectory:
                    filentitles[filename] = 0

                if filename in filentitles:
                    print("two file found with same name. input new name. old name:", filename)
                    k = input()
                    while True:
                        if k in filentitles:
                            print("all ready named file", k, ". choose new name")
                            k = input()

                        else:
                            break

                    filentitles[k] = 0
                    apath = newDirectory + "/" + k
                    os.mkdir(apath)

                else:
                    filentitles[filename] = 0
                    apath = newDirectory + "/" + filename
                    try:
                        os.mkdir(apath)
                    except FileExistsError:
                        print("file already named that. made copy")
                        copyAmount = 0
                        while True:
                            try:
                                os.mkdir(newDirectory + "/" + filename + str(copyAmount))

                            except:
                                copyAmount += 1
                                if copyAmount > 100:
                                    raise FileExistsError("warning: over 100 copy of",(newDirectory + "/" + filename), ". auto stopping")


                            else:
                                print("copy made")
                                break

        print(filentitles)

        if layer == 1:
            for names in filentitles:
                counter = 0

                for file in os.listdir(directory + "/" + names):
                    if file.endswith((".jpg", ".png")):
                        print(file)
                        newImage = changeImage(os.path.join((directory + "/" + names), file), settings[0], settings[1],
                                               settings[2])
                        holder = (newDirectory + "/" + names + "/" + str(counter) + ".jpg")
                        cv.imwrite(holder, newImage)
                        counter += 1



        elif layer == 0:
            for file in os.listdir(directory):
                if file.endswith((".jpg", ".png")):
                    print(file)
                    newImage = changeImage(os.path.join(directory, file), settings[0], settings[1], settings[2]
                                           )
                    holder = (newDirectory + "/" + "copy.jpg")
                    cv.imwrite(holder, newImage)

    print("finished")


def changeImage(directory, show=False, dim=(244, 244), localizes=True):  # Change images to selected size and grey scale.
    window_name = 'Image'

    if not path.exists(directory):
        raise Exception("cvImageChanger: findImage: no file exists, check location")

    image = cv.imread(
        directory)

    resized = cv.resize(image, dim,
                        interpolation=cv.INTER_AREA)

    if show:
        print("press 'ESC' to exit")
        cv.imshow(window_name, image)  # shows image ?remove or make command based
        i = cv.waitKey(0)
        if (i == "ESC"):
            cv.destroyAllWindows()

    grey_image = cv.cvtColor(resized, cv.COLOR_RGB2GRAY)  # changes to grey

    if show:
        print("press 'ESC' to exit")
        cv.imshow(window_name, grey_image)  # shows image ?remove or make command based
        i = cv.waitKey(0)
        if (i == "ESC"):
            cv.destroyAllWindows()

    if localizes:
        image = Localize(grey_image)

    if show:
        print("press 'ESC' to exit")
        cv.imshow(window_name, image)  # shows image ?remove or make command based
        i = cv.waitKey(0)
        if (i == "ESC"):
            cv.destroyAllWindows()

    return image


def Localize(img):  # https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html - Otsu's Binarization
    ret2, th2 = cv.threshold(img, 0, 255,
                             cv.THRESH_BINARY + cv.THRESH_OTSU)  # cvThreshold(image, binary_image,128,255,CV_THRESH_OTSU)

    return th2



files("C:/Users/gamin/Desktop/dataset sorted", "C:/Users/gamin/Desktop/test_file", layer=1)


#a = changeImage("C:/Users/gamin/Desktop/final project/test3.JPG")

#cv.imwrite("C:/Users/gamin/OneDrive/Desktop/final project/TEST3.JGP", a)
