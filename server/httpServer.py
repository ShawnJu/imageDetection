import posixpath
import BaseHTTPServer
import urllib
import cgi
import shutil
import mimetypes
import re

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


class SimpleHTTPRequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """Simple HTTP request handler with GET/HEAD/POST commands.

    This serves files from the current directory and any of its
    subdirectories.  The MIME type for files is determined by
    calling the .guess_type() method. And can reveive file uploaded
    by client.

    The GET/HEAD/POST requests are identical except that the HEAD
    request omits the actual contents of the file.

    """

    # server_version = "SimpleHTTPWithUpload/" + __version__

    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        if f:
            f.close()

    def do_POST(self):
        """Serve a POST request."""
        r, info = self.deal_post_data()
        print info, " by: ", self.client_address
        f = StringIO()
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write("<html>\n<title>Upload Result Page</title>\n")
        f.write("<body>\n<h2>Upload Result Page</h2>\n")
        f.write("<hr>\n")
        if r:
            f.write("<strong>Success: </strong>")
        else:
            f.write("<strong>Failed: </strong>")
        f.write(info)
        f.write("<br><a href=\"%s\">back</a>" % self.headers['referer'])
        f.write("<hr><small>ShawnJu aka. go fuck  yourself")
        f.write("<a>")
        f.write("</a>.</small></body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    # def deal_post_data(self):
    #     boundary = self.headers.plisttext.split("=")[1]
    #     remainbytes = int(self.headers['content-length'])
    #     line = self.rfile.readline()
    #     remainbytes -= len(line)
    #     if not boundary in line:
    #         return (False, "Content NOT begin with boundary")
    #     line = self.rfile.readline()
    #     remainbytes -= len(line)
    #     fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line)
    #     if not fn:
    #         return (False, "Can't find out file name...")
    #     path = self.translate_path(self.path)
    #     fn = os.path.join(path, fn[0])
    #     line = self.rfile.readline()
    #     remainbytes -= len(line)
    #     line = self.rfile.readline()
    #     remainbytes -= len(line)
    #     try:
    #         out = open(fn, 'wb')
    #     except IOError:
    #         return (False, "Can't create file to write, do you have permission to write?")
    #     preline = self.rfile.readline()
    #     remainbytes -= len(preline)
    #     while remainbytes > 0:
    #         line = self.rfile.readline()
    #         remainbytes -= len(line)
    #         if boundary in line:
    #             preline = preline[0:-1]
    #             if preline.endswith('\r'):
    #                 preline = preline[0:-1]
    #             out.write(preline)
    #             out.close()
    #             storagepath = path+"/storage/"
    #             if not os.path.exists(storagepath):
    #                 print("create storage folder "+storagepath)
    #                 os.mkdir(storagepath)
    #                 os.mkdir(storagepath+"untitled/")
    #             if os.path.exists("cache.png"):
    #                 os.remove("cache.png")
    #             try:
    #                 fix_orientation(fn)
    #                 face = process(fn)
    #                 face.save("cache.png")
    #                 print "saved cached.png"
    #                 faceArray = img_to_matrix("cache.png")
    #                 faceArray = pcamodel.transform(faceArray)
    #                 prediction = svmmodel.predict(faceArray)
    #                 if not os.path.exists(storagepath+prediction[0]):
    #                     os.mkdir(storagepath+prediction[0])
    #                 shutil.copy2(fn, storagepath+prediction[0])
    #                 print(prediction)
    #             except:
    #                 print("dude you have no face")
    #                 shutil.copy2(fn, storagepath+"untitled/")
    #                 print("We store your upload in untitled!!")
    #                 os.remove(fn)
    #                 continue
    #             os.remove(fn)
    #             print("cleaned up cache")
    #             return (True, "File upload success! your are %s!! We store your file under the same folder as your name" % prediction)
    #         else:
    #             out.write(preline)
    #             preline = line
    #     return (False, "Unexpect Ends of data.")




    def deal_post_data(self):
        boundary = self.headers.plisttext.split("=")[1]
        remainbytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            return (False, "Content NOT begin with boundary")
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(r'Content-Disposition.*name="file"; filename="(.*)"', line)
        if not fn:
            return (False, "Can't find out file name...")
        path = self.translate_path(self.path)
        fn = os.path.join(path, fn[0])
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            return (False, "Can't create file to write, do you have permission to write?")
        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith('\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                print(fn)
                storagepath = path+"/storage/"
                if not os.path.exists(storagepath):
                    print("create storage folder "+storagepath)
                    os.mkdir(storagepath)
                    os.mkdir(storagepath+"untitled/")
                if os.path.exists("cache.png"):
                    os.remove("cache.png")
                try:
                    # fix_orientation(fn)
                    print
                except:
                    print "we cannot rotate it"

                try:
                    face = process(fn)
                    face.save("cache.png")
                    print "saved cached.png"
                except:
                    print "cannot find the cache png"
                try:
                    faceArray = img_to_matrix("cache.png")
                    # print("before transformation ", faceArray)
                    faceArray = pcamodel.transform(faceArray)
                    # print("after transformation ", faceArray)
                    prediction = svmmodel.predict(faceArray)
                except:
                    # print "cannot print predection"
                    print ""
                try:
                    if not os.path.exists(storagepath+prediction[0]):
                        os.mkdir(storagepath+prediction[0])
                    shutil.copy2(fn, storagepath+prediction[0])
                except:
                    print("dude you have no face")
                    shutil.copy2(fn, storagepath+"untitled/")
                    print("We store your upload in untitled!!")
                    os.remove(fn)
                    continue
                print("I think you are " + str(prediction))
                os.remove(fn)
                print("cleaned up cache")
                return (True, "File upload success! your are %s!! We store your file under the same folder as your name" % prediction)
            else:
                out.write(preline)
                preline = line
        return (False, "Unexpect Ends of data.")

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f

    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        list.sort(key=lambda a: a.lower())
        f = StringIO()
        displaypath = cgi.escape(urllib.unquote(self.path))
        f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">')
        f.write("<html>\n<title>Directory listing for %s</title>\n" % displaypath)
        f.write("<body>\n<h2>Directory listing for %s</h2>\n" % displaypath)
        f.write("<hr>\n")
        f.write("<form ENCTYPE=\"multipart/form-data\" method=\"post\">")
        f.write("<input name=\"file\" type=\"file\"/>")
        f.write("<input type=\"submit\" value=\"upload\"/></form>\n")
        f.write("<hr>\n<ul>\n")
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            f.write('<li><a href="%s">%s</a>\n'
                    % (urllib.quote(linkname), cgi.escape(displayname)))
        f.write("</ul>\n<hr>\n</body>\n</html>\n")
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path

    def copyfile(self, source, outputfile):
        """Copy all data between two file objects.

        The SOURCE argument is a file object open for reading
        (or anything with a read() method) and the DESTINATION
        argument is a file object open for writing (or
        anything with a write() method).

        The only reason for overriding this would be to change
        the block size or perhaps to replace newlines by CRLF
        -- note however that this the default server uses this
        to copy binary data as well.

        """
        shutil.copyfileobj(source, outputfile)

    def guess_type(self, path):
        """Guess the type of a file.

        Argument is a PATH (a filename).

        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.

        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.

        """

        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    if not mimetypes.inited:
        mimetypes.init()  # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream',  # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
    })


def test(server_class=SimpleHTTPRequestHandler):
    print("Starting http server!!!")
    server = BaseHTTPServer.HTTPServer(("0.0.0.0", 8000), server_class)
    server.serve_forever()
    # BaseHTTPServer.test(handler_class, server_class)


#########GOOD LUCK###########

from PIL import Image, ImageFile
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
    if verbose == True:
        print "changing size from %s to %s" % (str(img.size), str(STANDARD_SIZE))
    ret = np.asarray(list(img.getdata()))
    return ret


def load_data():
    img_dir = "./temp/"
    images = []
    for f in os.listdir(img_dir):
        if f.startswith("."):
            continue
        images.append(img_dir + f)
    print(images)
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
    print("Start compressing signals!!!")
    for image in images:
        print "loading ... "+ image
        if (image.endswith("_Store")):
            continue
        img = img_to_matrix(image)
        data.append(img)
    labels = np.array(labels)
    ret = np.asarray(data)
    return ret, labels

# def load_data():
#     img_dir = "./temp/"
#     images = []
#     for f in os.listdir(img_dir):
#         if f.startswith("."):
#             continue
#         images.append(img_dir+f)
#     print(images)
#     labels = ["shangju" if "shangju" in f.split(' ')[0] else "xinkeliu" for f in images]
#     print(labels)
#     data = []
#     for image in images:
#         print image
#         if(image.endswith("_Store")):
#             continue
#         img = img_to_matrix(image)
#         data.append(img)
#     data = np.array(data)
#     return data, labels

def pcaPic(data, label):
    n_components = 100
    print("Data dimension: "+  str(data.shape))
    print("Reconstructing compressed signal!!!")
    pca = RandomizedPCA(n_components=n_components, whiten=True).fit(data)
    X_train_pca = pca.fit_transform(data)
    y_train = label
    print("Learning reconstructed image!!!")
    param_grid = {'C': [1e3, 5e3, 1e4, 5e4, 1e5],
                  'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1], }
    clf = GridSearchCV(SVC(kernel='rbf', class_weight='auto'), param_grid)
    clf = clf.fit(X_train_pca, y_train)
    return pca, clf


##########HAVE SOME FUN############
import os
import cv2


def detect_object(image):
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(
        "/usr/local/Cellar/opencv/2.4.11/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml")
    rect = cascade.detectMultiScale(grayscale, scaleFactor=1.2, minNeighbors=2, flags=cv2.cv.CV_HAAR_SCALE_IMAGE,
                                    minSize=(100, 100))
    result = []
    print(rect)
    for (x, y, w, h) in rect:
        result.append((x, y, x + w, y + h))
    print "your face at" + str(result)
    return result


def process(infile):
    size = 250, 250
    image = cv2.imread(infile)
    faces = detect_object(image)
    im = Image.open(infile).convert('L')
    if faces:
        f = faces[0]
        a = im.crop(f)
        a.thumbnail(size, Image.ANTIALIAS)
        return a
    return


def buildModel():
    data, label = load_data()
    return pcaPic(data, label)


pcamodel, svmmodel = buildModel()

ImageFile.MAXBLOCK = 1024 * 1024 * 1024

# The EXIF tag that holds orientation data.
EXIF_ORIENTATION_TAG = 274

# Obviously the only ones to process are 3, 6 and 8.
# All are documented here for thoroughness.
ORIENTATIONS = {
    1: ("Normal", 0),
    2: ("Mirrored left-to-right", 0),
    3: ("Rotated 180 degrees", 180),
    4: ("Mirrored top-to-bottom", 0),
    5: ("Mirrored along top-left diagonal", 0),
    6: ("Rotated 90 degrees", -90),
    7: ("Mirrored along top-right diagonal", 0),
    8: ("Rotated 270 degrees", -270)
}


def fix_orientation(img, save_over=True):
    """
    `img` can be an Image instance or a path to an image file.
    `save_over` indicates if the original image file should be replaced by the new image.
    * Note: `save_over` is only valid if `img` is a file path.
    """
    path = None
    if not isinstance(img, Image.Image):
        path = img
        img = Image.open(path)
    elif save_over:
        raise ValueError("You can't use `save_over` when passing an Image instance.  Use a file path instead.")
    try:
        orientation = img._getexif()[EXIF_ORIENTATION_TAG]
    except (TypeError, AttributeError, KeyError):
        raise ValueError("Image file has no EXIF data.")
    if orientation in [3, 6, 8]:
        degrees = ORIENTATIONS[orientation][1]
        img = img.rotate(degrees)
        if save_over and path is not None:
            try:
                img.save(path, quality=95)
            except IOError:
                # Try again, without optimization (PIL can't optimize an image
                # larger than ImageFile.MAXBLOCK, which is 64k by default).
                # Setting ImageFile.MAXBLOCK should fix this....but who knows.
                img.save(path, quality=95)
        return (img, degrees)
    else:
        print "wtf?"
        return (img, 0)

####have some fun###
if __name__ == '__main__':
    test()