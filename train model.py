import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model
import os
import shutil
import random
from os import listdir
from os.path import isfile, join


def file_maker(location, topEnd):
    os.chdir(location)
    try:
        os.mkdir("train")
        os.mkdir("valid")
        os.mkdir("test")

    except FileExistsError:
        print("warning file already found")

    for num in range(0, topEnd):
        try:
            os.mkdir("train/" + str(num))
            os.mkdir("valid/" + str(num))
            os.mkdir("test/" + str(num))

        except FileExistsError:
            print("warning file", num, " already found")
            pass

    print("files finished")


def randomSort(location, fileTotal=10, SampleSize=30, testSampleSize=5): #30 5
    paths = {"trainPath": str,
             "validPath": str,
             "testPath": str}

    for z in range(0, fileTotal):

        onlyFiles = [f for f in listdir(location + "/train/" + str(z)) if
                     isfile(join(location + ("/train/" + str(z)), f))]  # finds all files in dict

        samples = random.sample(onlyFiles, SampleSize)
        print("samples", samples)
        for j in samples:  # select all random file to be moved
            shutil.move(location + "/train/" + str(z) + "/" + j,
                        location + "/valid/" + str(z))  # moves from train to test

        onlyFiles = [f for f in listdir(location + "/train/" + str(z)) if
                     isfile(join(location + "/train/" + str(z), f))]  # finds all files in dict again as some moved

        test_samples = random.sample(onlyFiles, testSampleSize)
        for k in test_samples:
            shutil.move(location + "/train/" + str(z) + "/" + k, location + "/test/" + str(z))

    paths["trainPath"] = location + "/train"
    paths["validPath"] = location + "/valid"
    paths["testPath"] = location + "/test"

    print("random sort done")
    return paths


def process(fileL, layers=10, saved=False, savedName="my_model"):
    tBatch = ImageDataGenerator(
        preprocessing_function=tf.keras.applications.mobilenet.preprocess_input).flow_from_directory(
        directory=fileL["trainPath"], target_size=(224, 224), batch_size=10)
    vBatches = ImageDataGenerator(
        preprocessing_function=tf.keras.applications.mobilenet.preprocess_input).flow_from_directory(
        directory=fileL["validPath"], target_size=(224, 224), batch_size=10)

    mn_mobile = tf.keras.applications.mobilenet.MobileNet()

    x = mn_mobile.layers[-6].output  # run tests

    out = Dense(units=layers, activation="softmax")(x)
    untrained_m = Model(inputs=mn_mobile.input, outputs=out)

    for layer in untrained_m.layers[:-2]:
        layer.trainable = False
    untrained_m.compile(loss="categorical_crossentropy", metrics=["accuracy"], optimizer=Adam(learning_rate=0.0001))

    x = input("view summary? (Y/N)")
    x.lower()
    if x == "y":
        untrained_m.summary()

    untrained_m.fit(x=tBatch,
                    steps_per_epoch=len(tBatch),
                    validation_data=vBatches,
                    validation_steps=len(vBatches),
                    epochs=25, #25
                    verbose=2,
                    )

    if saved:
        untrained_m.save("saved_model/" + savedName)
        print("NN saved as", savedName)
    else:
        print("nn not saved")

    print("nn finished")


def main():
    while True:
        print("")
        selection = input("please select 'file_maker' to produce images files,"
                          " 'random sort' randomly spilt images to different files, "
                          "'rprocess' to randomly split images and process model,  "
                          "'process' to process/train model"
                          "'exit' to end: ")
        selection.lower()
        if selection == "file_maker" or selection == "f":
            a = input("please input file location")
            b = input("please image types amount")
            file_maker(a, int(b))
        elif selection == "random sort" or selection == "r":
            a = input("please input file location")
            b = input("please image types amount")
            path = randomSort(a, int(b))
            print("paths:" + str(path))
        elif selection == "rprocess" or selection == "rp":
            a = input("please input file location")
            b = input("please image types amount")
            paths = randomSort(a, int(b))
            print("image done. processing model")
            q = input("save model? (True/False)")
            q.capitalize()
            if q == "True":
                s = input("save model name? ")
                process(paths, int(b), saved=bool(q), savedName=s)
            else:
                process(paths, int(b))
        elif selection == "process" or selection == "p":
            c = {"trainPath": str, "validPath": str}
            a = input("please input path for training")
            c["trainPath"] = a
            a = input("please input path for valid")
            c["validPath"] = a
            b = input("please image types amount")
            q = input("save model? (True/False)")
            q.capitalize()
            if q == "True":
                s = input("save model name? ")
                process(c, int(b), saved=bool(q), savedName=s)
            else:
                process(c, int(b))

        elif selection == "exit" or selection == "e":
            break
        else:
            print("error, option not selected. try again.")
            print("")

    quit()


if __name__ == "__main__":
    main()
