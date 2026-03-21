from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense

model = Sequential()

model.add(Conv2D(32,(3,3),input_shape=(224,224,3)))
model.add(Flatten())
model.add(Dense(2,activation="softmax"))

model.save("artifacts/Model_Training/Trained_Model.h5")

print("Model created successfully")