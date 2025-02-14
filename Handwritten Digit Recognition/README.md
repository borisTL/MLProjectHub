# Handwritten Digit Recognition using Softmax, Perceptron, and Linear Regression

## Overview
This project implements **handwritten digit recognition** using three different machine learning models:
- **Softmax Regression**
- **Perceptron Algorithm**
- **Linear Regression**

The goal is to classify digits from the **MNIST dataset** using these methods, compare their performances, and analyze their effectiveness in digit recognition.

## Dataset
The project uses the **MNIST dataset**, which consists of **70,000 grayscale images** of handwritten digits (0-9). Each image has a size of **28x28 pixels** and is labeled accordingly.

## Models Implemented
### 1. Softmax Regression
- A generalization of logistic regression for multi-class classification.
- Computes probability scores for each digit and selects the highest probability as the predicted class.
- Optimized using **gradient descent**.

### 2. Perceptron Algorithm
- A simple **binary classifier**, extended for multi-class classification using the **one-vs-all (OvA) strategy**.
- Uses **step function** as activation.
- Updates weights based on misclassification.

### 3. Linear Regression
- A regression model used for classification by assigning the highest predicted value as the class.
- Though not ideal for classification, it is implemented for comparison.
- Optimized using **least squares approach**.

## Implementation Details
- The models are **implemented from scratch** without using pre-built classifiers.
- Uses **vectorized operations** for efficiency.
- Performance is evaluated using:
  - **Accuracy**
  - **Confusion Matrix**
  - **Sensitivity Analysis**

## Performance Evaluation
The models are tested on a **test dataset**, and their accuracy and confusion matrices are analyzed to determine:
- Which model performs best for digit recognition.
- The strengths and weaknesses of each approach.

## Requirements
To run this project, you need:
- Python 3.x
- Jupyter Notebook
- NumPy
- Pandas
- Matplotlib
- Scikit-learn (for data preprocessing)

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/borisTL/Handwritten-Digit-Recognition.git
   cd Handwritten-Digit-Recognition
   ```
2. Install dependencies:
   ```bash
   pip install numpy pandas matplotlib scikit-learn
   ```
3. Open the Jupyter Notebook:
   ```bash
   jupyter notebook "Handwritten Digit Recognition using Softmax, Perceptron, and Linear Regression.ipynb"
   ```
4. Run all cells and analyze the results.

## Results & Analysis
- **Softmax Regression** provides the best accuracy due to probabilistic classification.
- **Perceptron** works well but struggles with overlapping digits.
- **Linear Regression** is the weakest since it's not designed for classification.

## Future Improvements
- Implementing **Neural Networks (MLP) for better accuracy**.
- Using **CNNs (Convolutional Neural Networks)** to capture spatial relationships in images.
- Adding **regularization** to improve generalization.

## Author
**Boris Teplitskiy**
- GitHub: [borisTL](https://github.com/borisTL)
- LinkedIn: [Boris Teplitskiy](https://www.linkedin.com/in/boris-teplitskiy-54a490249/)

---
### If you find this project useful, feel free to ⭐ the repository and contribute!

