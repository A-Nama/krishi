# KRISHI: An Annotated Dataset for Agricultural Text Classification in Malayalam 

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This repository contains the official dataset and baseline model implementations for our paper, **"KRISHI: An Annotated Dataset for Agricultural Text Classification in Malayalam"**.

Our work aims to address the scarcity of NLP resources for the agricultural domain in low-resource Indian languages, starting with Malayalam.

---
## About the Dataset 

The KRISHI dataset is a collection of agricultural texts in Malayalam, expertly annotated into five distinct categories. It is designed to serve as a benchmark for developing and evaluating NLP models for agricultural applications in the region.

The five categories are:
* `AGRI_PRACTICES`
* `CROPS`
* `DISEASES`
* `ENVIRONMENTAL_FACTORS`
* `LIVESTOCK`

### Access the Dataset

The dataset is a living resource and will be updated periodically with new data. You can access the latest version via the Google Sheet linked below.

**➡️ [Access the KRISHI Dataset (Google Sheet)](https://docs.google.com/spreadsheets/d/1hTUw3fPDvqC2f2LYX9bDVuxKx_R1F_kRkbk__QsMvEg/edit?usp=sharing)**


---
## Baseline Models & Results

We established baseline performance on the KRISHI dataset using three standard machine learning algorithms. Our results highlight that while class imbalance poses a challenge for probabilistic models, margin-based approaches demonstrated significant robustness.

| Model | Accuracy | Weighted F1-Score |
| :--- | :---: | :---: |
| **SVM (LinearSVC)** | **69%** | **0.68** |
| Logistic Regression | 55% | 0.47 |
| Naive Bayes | 45% | 0.30 |

**Key Insights:**
* **LinearSVC** achieved the strongest performance, effectively handling minority classes like `DISEASES` (F1: 0.91) and `LIVESTOCK` (F1: 0.80) where other models struggled.
* **Logistic Regression** and **Naive Bayes** showed a strong bias towards the majority `CROPS` class, resulting in significantly lower performance on underrepresented categories.

---
