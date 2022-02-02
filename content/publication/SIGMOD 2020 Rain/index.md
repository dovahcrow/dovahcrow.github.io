---
title: "Complaint-driven Training Data Debugging for Query 2.0"
authors:
  - Weiyuan Wu
  - Lampros Flokas
  - Eugene Wu
  - Jiannan Wang

date: "2019-04-01"
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: "2020-04-01"

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["1"]

# Publication name and optional abbreviated publication name.
publication: "SIGMOD 2020"
publication_short: "SIGMOD 2020"

abstract: >
  As the need for machine learning (ML) increases rapidly across all industry sectors,
  there is a significant interest among commercial database providers to support "Query 2.0",
  which integrates model inference into SQL queries.
  Debugging Query 2.0 is very challenging since an unexpected query result may be caused by the bugs in training data (e.g., wrong labels, corrupted features).
  In response, we propose Rain, a complaint-driven training data debugging system.
  Rain allows users to specify complaints over the query's intermediate or final output,
  and aims to return a minimum set of training examples so that if they were removed, the complaints would be resolved.
  To the best of our knowledge, we are the first to study this problem. A naive solution requires retraining an exponential number of ML models.
  We propose two novel heuristic approaches based on influence functions which both require linear retraining steps.
  We provide an in-depth analytical and empirical analysis of the two approaches and conduct extensive experiments to evaluate their effectiveness using four real-world datasets.
  Results show that Rain achieves the highest recall@k among all the baselines while still returns results interactively.  

# Summary. An optional shortened abstract.
summary: ""

tags:
- Data Cleaning
- Data Debugging
- ML Debugging
featured: false

links:
  - name: arXiv
    url: https://arxiv.org/abs/2004.05722
    
url_pdf: http://arxiv.org/pdf/2004.05722
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