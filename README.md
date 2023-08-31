# Introduction

Hello there! You have stumbled upon my machine learning project archive, where I upload all of the machine learning projects that I have worked on. There is material ranging from academic projects to mini machine learning exercises to project showcases. 

# Table of Contents

- [Project Showcase](#Project-Showcase)
  - [Sea of News](#SEA-of-News)
- [Academic Projects](#Academic-Projects)
  - [Pain Detection](#Pain-Detection)
  - [Singapore Weather Prediction](#Singapore-Weather-Prediction)
- [Machine Learning Projects](#Machine-Learning-Projects)
  - [Singapore Energy Usage](#Singapore-Energy-Usage)
  - [Rohingya Refugee Crisis](#Rohingya-Refugee-Crisis)


# Project Showcase
This section is where my best machine learning projects are displayed. In this section, you will find entire data pipelines which culminate to a final machine learning model. Here are the projects which I have displayed:

### SEA of News 
A summarization project whereby a web scraper is developed to scrape news from news outlets in Southeast Asia, daily and to summarize the articles. The headlines, date, outlet, etc. are collected as data and stored in an SQLite3 database, while the articles are then summarized accordingly. The summarized articles are then generated into a PDF for easy viewing. This entire project is dedicated to geopolitical analysts or anyone who reads the news in order to get a brief overview of the news in other countries. What makes this project stand out is that it is relatively easy to change the script to make it applicable to other countries in the world and its' news outlets, as well as having the goal to make future research more efficient. This project is an ongoing process and is continuously updated.

# Academic Projects
This section is where my academic projects, and the projects that I did back in university are displayed. Here are the projects which I have displayed:

### Pain Detection
People who have dementia often have difficulties expressing pain through their facial expressions. In this project, myself and two others, compared two cutting-edge computer vision deep learning architectures to classify the pain levels in people with dementia. This was done using the PSPI score as a metric to classify pain levels and the use of GPUs to train the model. Finally, a final report was written which achieved a grade of A. This project was written for the class CSC413: Neural Networks and Deep Learning at the University of Toronto.

### Singapore Weather Prediction
An implementation of the paper "Rainfall Monthly Prediction Based on Artificial Neural Network – A Case Study Tenggarong Station, East Kalimantan – Indonesia" by Mislan et al. The goal of this project is to adapt this algorithm, designed to predict rainfall in Indonesia to the rainfall patterns in Singapore. I changed the optimization from Levenberg-Marquardt to Adam and obtained a lower training loss. However, there are signs of overfitting in the final result.

# Machine Learning Mini Projects
This section is where my machine learning exercises are displayed, usually using datasets taken from Kaggle. Here are the projects which I have displayed:

### Singapore Energy Usage
Used and compared two regression models, Ridge and Simple linear regression in order to predict and find out the factors that contribute to energy usage in buildings in Singapore. The Ridge model differs from the Simple linear regression model because of the addition of a penalty term, which penalizes high numbers of parameters, keeping the model more simple. The results found that the Ridge Model was preferable because I wanted to keep explanations simple.

### Rohingya Refugee Crisis
The Rohingya are an Muslim ethnic group located in the border between Bangladesh and Myanmar. In recent times, they have been the target of anti-Muslim terror groups which led to an exodus into Bangladesh. In this project, I aim to classify the confidence levels of Rohingya refugees as to find the factors which influence refugee confidence in their temporary homes. I hope that these results will help inform governmental institutions on how best to manage refugees. The method was to use decision trees, XGBoost and random forests, after exploratory data analysis, in order to start the classification. The final result found that XGBoost gave the best accuracy result at around 69% with the others slightly below that. Finally, it was found that the factors which contributed the most to managing refugee confidence are income satisfaction, access to help, religious facilities, camp conditions and if the government in Myanmar will recognize Rohingya rights.
