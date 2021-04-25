# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow import keras

# Helper libraries
import numpy as np
import matplotlib.pyplot as plt

#导入图像数据集
fashion_mnist = keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

#10个类别的名称
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

"""
#浏览训练集和测试集的数据
train_images.shape
len(train_labels)
train_labels

#查看第一张训练集图片
plt.figure()
plt.imshow(train_images[0])
plt.colorbar()
plt.grid(False)
plt.show()

#处理测试和训练的图片
train_images = train_images / 255.0
test_images = test_images / 255.0

#显示训练集中的前25个图像，并显示类名
plt.figure(figsize=(10,10))
for i in range(25):
    plt.subplot(5,5,i+1)
    plt.xticks([])
    plt.yticks([])
    plt.grid(False)
    plt.imshow(train_images[i], cmap=plt.cm.binary)
    plt.xlabel(class_names[train_labels[i]])
plt.show()
"""

#1.构建网络
#1.1设置神经网络的层
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)), #网络的第一层
    keras.layers.Dense(128, activation='relu'), #第一个Dense层，全连接神经层，有128个节点
    keras.layers.Dense(10)
    #第二个（最后一个）层，返回一个长度为10的logits数组，每个节点都包含一个得分用来表示图像所属类别
])

#1.2编译模型的设置
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

#2.训练模型
#2.1向模型馈送数据
model.fit(train_images, train_labels, epochs=10)
#训练期间会显示损失和准确率

#2.2评估模型的准确率
test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
print('\nTest accuracy:', test_acc)

#2.3进行预测，添加Softmax层，将logits转换为概率
probability_model = tf.keras.Sequential([model, 
                                         tf.keras.layers.Softmax()])

predictions = probability_model.predict(test_images)

#第一个预测结果
print(predictions[0])
print(np.argmax(predictions[0]))