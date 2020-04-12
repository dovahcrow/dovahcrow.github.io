---
title: "Complaint-driven Training Data Debugging for Query 2.0"
authors:
  - admin
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
publication_types: ["3"]

# Publication name and optional abbreviated publication name.
publication: "SIGMOD 2020"
publication_short: "SIGMOD 2020"

abstract: >
  As the need for machine learning (ML) increases rapidlyacross all industry sectors, 
  there is a significant interestamong commercial database providers to support “Query2.0”, 
  which integrates model inference into SQL queries. 
  Debugging Query 2.0 is very challenging since an unexpectedquery result may be caused by the bugs in training data (e.g.,wrong labels, corrupted features).
  In response, we propose Rain, a complaint-driven training data debugging system.
  Rain allows users to specify complaints over the query’sintermediate or final output, 
  and aims to return a minimumset of training examples so that if they were removed, the complaints would be resolved. 
  To the best of our knowledge, we are the first to study this problem. 
  A naive solution re-quires retraining an exponential number of ML models. 
  Wepropose two novel heuristic approaches based on influencefunctions which both require linear retraining steps. 
  We provide an in-depth analytical and empirical analysis of the twoapproaches and conduct extensive experiments to evaluatetheir effectiveness using four real-world datasets. 
  Resultsshow thatRainachieves the highest recall@k among all thebaselines while still returns results interactively

# Summary. An optional shortened abstract.
summary: ""

tags:
- Explanation
featured: false

links:
- name: arXiv Version
  url: files/Rain-arXiv.pdf
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