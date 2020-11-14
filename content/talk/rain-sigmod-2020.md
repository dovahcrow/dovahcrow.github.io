---
abstract: >
  As the need for machine learning (ML) increases rapidly across all industry sectors, 
  there is a significant interest among commercial database providers to support "Query 2.0", 
  which integrates model inference into SQL queries. Debugging Query 2.0 is very challenging
  since an unexpected query result may be caused by the bugs in training data (e.g., wrong labels, corrupted features).
  In response, we propose Rain, a complaint-driven training data debugging system. 
  Rain allows users to specify complaints over the query's intermediate or final output, 
  and aims to return a minimum set of training examples so that if they were removed, the complaints would be resolved.
  To the best of our knowledge, we are the first to study this problem. 
  A naive solution requires retraining an exponential number of ML models. 
  We propose two novel heuristic approaches based on influence functions which both require linear retraining steps. 
  We provide an in-depth analytical and empirical analysis of the two approaches and conduct extensive experiments 
  to evaluate their effectiveness using four real-world datasets. 
  Results show that Rain achieves the highest recall@k among all the baselines while still returns results interactively.
categories:
  - talk
date: 2020-06-17T00:00:00+08:00
time_start: 2020-06-17T00:00:00+08:00
time_end: 2020-06-17T00:00:00+08:00
event: "SIGMOD 2020"
event_url: "https://sigmod2020.org/"
highlight: true
location: "Zoom"
tags: 
  - rain
  - machine learning debugging
  - SQL explanation
title: Complaint-driven Training Data Debugging
url_pdf: ""
url_slides: ""
url_video: "https://www.youtube.com/watch?v=qvgBmM1LP38&list=PLuJUUc5MHC2A9lUxFGrNvZeX_hgQ4I1Jq&index=10"

# Is this a selected talk? (true/false)
selected: true


# Does the content use math formatting?
math: false

# Does the content use source code highlighting?
highlight: false

# Featured image
# Place your image in the `static/img/` folder and reference its filename below, e.g. `image = "example.jpg"`.
header:
  image: ""
  caption: ""

  # Projects (optional).
#   Associate this talk with one or more of your projects.
#   Simply enter the filename (excluding '.md') of your project file in `content/project/`.
projects: []
---
