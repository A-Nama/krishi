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

For a static version used in our paper, please see the `/data` directory in this repository.

---
## Baseline Models & Results 

We established baseline performance on the KRISHI dataset using two prominent transformer models. Our results highlight the challenge of class imbalance and the advantage of language-specific pre-training.

| Model | Accuracy | Weighted F1-Score |
| :--- | :---: | :---: |
| `ai4bharat/indic-bert` | **53%** | **0.45** |
| `bert-base-multilingual-cased` | 47% | 0.30 |

The superior performance of `indic-bert` demonstrates the value of using language-specific models for this task.

---
