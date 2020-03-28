from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Image
from .forms import UploadFileForm
from django.shortcuts import redirect

import os
import shutil
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, MaxPooling2D
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

# Create your views here.
def home_index_view(request):
    form = UploadFileForm()
    pred = ''
    img =''
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            img = request.FILES['img']
            shutil.rmtree("media/images")
            os.mkdir("media/images")
            form.save()
            class_names = ['building', 'forest', 'glacier', 'mountain', 'sea','street']
            pred = handle_uploaded_file(img)
            pred = class_names[pred]
            print(img)
            img = str(img)
    else:
        form = UploadFileForm()
    context = {
        "form" : form,
        "pred" : pred,
         "img" : img
    }
    return render(request, 'index.html', context)
            
def handle_uploaded_file(f):
    model = Sequential([
        Conv2D(32, 3, padding='same', activation='relu', input_shape=(150, 150, 3)),
        MaxPooling2D(),
        Conv2D(64, 3, padding='same', activation='relu'),
        MaxPooling2D(),
        Conv2D(96, 3, padding='same', activation='relu'),
        Conv2D(96, 3, padding='same', activation='relu'),
        Conv2D(64, 3, padding='same', activation='relu'),
        MaxPooling2D(),
        Flatten(),
        Dense(1024, activation='relu'),
        Dropout(0.5),
        Dense(1024, activation='relu'),
        Dropout(0.5),
        Dense(6)
    ])
    model.load_weights(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"home/model_weights.h5"))
    image = Image.open(f)
    new_image = image.resize((150, 150))
    nppic = np.array(new_image).astype('float16').reshape(1,150,150,3)
    pred = model.predict_classes(nppic)[0]
    print("this picture is categorized as {}".format(pred))
    return pred