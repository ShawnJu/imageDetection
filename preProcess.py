__author__ = 'ShangJu'


from PIL import Image
import os
import numpy as np
from sklearn.decomposition import RandomizedPCA
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC


STANDARD_SIZE = (512, 512)

def img_to_matrix(filename, verbose=False):
    """
    takes a filename and turns it into a numpy array of RGB pixels
    """
    img = Image.open(filename)
    if verbose==True:
        print "changing size from %s to %s" % (str(img.size), str(STANDARD_SIZE))
    ret =  np.asarray(list(img.getdata()))
    return ret

def load_data():
    img_dir = "./temp/"
    images = []
    for f in os.listdir(img_dir):
        if f.startswith("."):
            continue
        images.append(img_dir+f)
    print(images)
    # labels = ["shangju" if "shangju" in f.split(' ')[0] else "xinkeliu" for f in images]
    labels = []
    for f in images:
        x = f.split(' ')[0]
        if "shangju" in x:
            labels.append("ShawnJu")
        elif "xinkeliu" in x:
            labels.append("XinkeLiu")
        elif "feifeizhang" in x:
            labels.append("FeifeiZhang")
    # labels = ["ShawnJu" if "shangju" in f.split(' ')[0] else "XinkeLiu" for f in images]
    print(labels)
    data = []
    for image in images:
        print image
        if(image.endswith("_Store")):
            continue
        img = img_to_matrix(image)
        data.append(img)
    data = np.array(data)
    return data, labels

def pcaPic(data, label):
    n_components =100
    print(data.shape)
    print("train pca!!")
    pca = RandomizedPCA(n_components=n_components, whiten=True).fit(data)
    X_train_pca = pca.fit_transform(data)
    y_train  = label
    print("Fitting the classifier to the training set")
    param_grid = {'C': [1e3, 5e3, 1e4, 5e4, 1e5],
              'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1], }
    clf = GridSearchCV(SVC(kernel='rbf', class_weight='auto'), param_grid)
    clf = clf.fit(X_train_pca, y_train)
    return pca, clf

def testing(pca, clf):
    while(True):
        path = raw_input("what is the path you want to test")
        try:
            img = img_to_matrix(path)
        except:
            continue
        img = pca.transform(img)
        prediction = clf.predict(img)
        print(prediction)




if __name__ == "__main__":
    data, label = load_data()
    pcaModel, clfModel = pcaPic(data,label)
    print("finish the model")
    testing(pcaModel, clfModel)