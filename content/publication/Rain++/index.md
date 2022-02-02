---
title: "Complaint-Driven Training Data Debugging at Interactive Speeds"
authors:
  - Lampros Flokas
  - Weiyuan Wu
  - Yejia Liu
  - Jiannan Wang
  - Nakul Verma
  - Eugene Wu

date: "2021-11-01"
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: "2020-11-01"

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["1"]

# Publication name and optional abbreviated publication name.
publication: "SIGMOD 2022"
publication_short: "SIGMOD 2022"

abstract: >
  Modern databases support queries that perform model inference (inference queries). Although powerful and widely used, inference queries are susceptible to incorrect results if the model is biased due to training data errors. Recently, Rain [40] proposed complaint-driven data debugging which uses user-specified errors in the output of inference queries (Complaints) to rank erroneous training examples that most likely caused the complaint. This can help users better interpret results and debug training sets. Rain combined influence analysis from the ML literature with relaxed query provenance polynomials from the DB literature to approximate the derivative of complaints w.r.t. training examples. Although effective, the runtime is O(|T|d), where T and d are the training set and model sizes, due to its reliance on the model’s second order derivatives (the Hessian). On a Wide Resnet Network (WRN) model with 1.5 million parameters, it takes >1 minute to debug a complaint.
  We observe that most complaint debugging costs are independent of the complaint, and that modern models are overparameterized. In response, Rain++ uses precomputation techniques, based on non-trivial insights unique to data debugging, to reduce debugging latencies to a constant factor independent of model size. We also develop optimizations when the queried database is known apriori, and for standing queries over streaming databases. Combining these optimizations in Rain++ ensures interactive debugging latencies (∼10ms) on models with millions of parameters.

# Summary. An optional shortened abstract.
summary: ""

tags:
- Data Cleaning
- Data Debugging
- ML Debugging
featured: false

url_pdf: files/Rain++.pdf

links:
# url_pdf: http://arxiv.org/pdf/1512.04133v1
# url_code: '#'
# url_dataset: '#'
# url_poster: '#'
# url_project: ''
# url_slides: ''
# url_source: '#'
# url_video: '#'

# Featured image
# To use, add an image named `featured.jpg/png` to your page's folder. 
image:
  caption: 'Image credit: [**Unsplash**](https://unsplash.com/photos/s9CC2SKySJM)'
  focal_point: ""
  preview_only: false

# Associated Projects (optional).
#   Associate this publication with one or more of your projects.
#   Simply enter your project's folder or file name without extension.
#   E.g. `internal-project` references `content/project/internal-project/index.md`.
#   Otherwise, set `projects: []`.
projects: []

# Slides (optional).
#   Associate this publication with Markdown slides.
#   Simply enter your slide deck's filename without extension.
#   E.g. `slides: "example"` references `content/slides/example/index.md`.
#   Otherwise, set `slides: ""`.
slides: ""
---