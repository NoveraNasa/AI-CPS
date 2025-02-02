# AI-Based Sentiment Analysis for Customer Reviews

## Overview

The project aims to develop an AI-based sentiment analysis system using customer reviews scraped from Booking.com.

This repository is developed as part of the course **M. Grum: Advanced AI-Based Application Systems** at **Potsdam University**. It showcases an end-to-end AI project that involves data scraping, preparation, training, validation, and deployment using **Docker and TensorFlow**. The goal is to create an AI-driven system that is fully reproducible and can be utilized by researchers and evaluators.

---

## Subgoals & Implementation

### **Subgoal 1: Git Usage**

- Forked the **MarcusGrum/AI-CPS** repository and modified it to fit our project needs.
- Maintained structured commits with meaningful messages (at least three per team member).
- Documented project ownership in this `README.md` file and clarified that this project is part of the **Advanced AI-Based Application Systems** course.

### **Subgoal 2: Data Scraping & Preparation**

- Scraped relevant data from the web and stored it in `joint_data_collection.csv`.
- Preprocessed data, including **outlier removal and normalization**.
- Split data into:
  - `training_data.csv` (80% of the dataset)
  - `test_data.csv` (20% of the dataset)
  - `activation_data.csv` (single entry from the test dataset)

### **Subgoal 3: Docker Images for Training & Activation**

- Created two **Docker images**:
  - `learningBase_SentimentAnalysis`: Contains training data (`training_data.csv`) at `/tmp/learningBase/train/` and test data (`test_data.csv`) at `/tmp/learningBase/validation/`.
  - `activationBase_SentimentAnalysis`: Contains activation data (`activation_data.csv`) at `/tmp/activationBase/`.
- Based images on **BusyBox** for lightweight deployment.
- Documented dataset origin and licensing in `README.md` inside Docker images.
- Verified functionality using `docker-compose.yml` and mounted external volume `ai_system`.

### **Subgoal 4: AI Model Training & Visualization**

- Developed an AI model using **TensorFlow**.
- Trained the model on `training_data.csv` and validated it using `test_data.csv`.
- Stored the trained model as `currentAiSolution.h5`.
- Saved **training metrics, loss, and accuracy** plots.
- Created visualization reports including:
  - Training and testing loss curves.
  - Diagnostic plots.
  - Scatter plots.

### **Subgoal 5: OLS Model for Comparison**

- Developed an **Ordinary Least Squares (OLS)** model using `statsmodels`.
- Trained and tested it using the same dataset for performance comparison.
- Stored the OLS model as `currentOlsSolution.pkl`.
- Documented performance using:
  - Diagnostic plots.
  - Scatter plots for analysis.

### **Subgoal 6: AI Model Deployment via Docker**

- Created two additional **Docker images**:
  - `knowledgeBase_SentimentAnalysis`: Contains the AI/OLS models at `/tmp/knowledgeBase/`.
  - `codeBase_SentimentAnalysis`: Provides activation data for AI inference.
- Documented ownership, course affiliation, model type, and **AGPL-3.0 license** in `README.md` inside Docker images.
- Published images on **Docker Hub** for accessibility.

### **Subgoal 7: Docker-Compose Utilization**

- Developed `docker-compose.yml` files for:
  1. Running the AI model using `knowledgeBase_SentimentAnalysis` and `activationBase_SentimentAnalysis`.
  2. Running the OLS model using the same setup.
- Used **external volume `ai_system`** for managing temporary files.
- Ensured seamless model execution by mounting required paths.

---

## Setup & Usage

### **1. Clone Repository**

```sh
git clone https://github.com/NoveraNasa/AI-Based-Sentiment-Analysis.git
cd AI-Based-Sentiment-Analysis
```
