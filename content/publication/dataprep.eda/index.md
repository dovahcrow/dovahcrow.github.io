---
title: "DataPrep.EDA: Task-Centric Exploratory Data Analysis for Statistical Modeling in Python"
authors: [Jinglin Peng, Weiyuan Wu, Brandon Lockhart, Song Bian, Jing Nathan Yan, Linghao Xu, Zhixuan Chi, Jeffrey Rzeszotarski, Jiannan Wang]

date: "2021-06-15"
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: "2021-06-15"

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["1"]

# Publication name and optional abbreviated publication name.
publication: "SIGMOD 2021"
publication_short: "SIGMOD 2021"

abstract: >
 Exploratory Data Analysis (EDA) is a crucial step in any data science project. However, existing Python libraries fall short in supporting data scientists to complete common EDA tasks for statistical modeling. Their API design is either too low level, which is optimized for plotting rather than EDA, or too high level, which is hard to specify more fine-grained EDA tasks. In response, we propose DataPrep.EDA, a novel task-centric EDA system in Python. DataPrep.EDA allows data scientists to declaratively specify a wide range of EDA tasks in different granularity with a single function call. We identify a number of challenges to implement DataPrep.EDA, and propose effective solutions to improve the scalability, usability, customizability of the system. In particular, we discuss some lessons learned from using Dask to build the data processing pipelines for EDA tasks and describe our approaches to accelerate the pipelines. We conduct extensive experiments to compare DataPrep.EDA with Pandas-profiling, the state-of-the-art EDA system in Python. The experiments show that DataPrep.EDA significantly outperforms Pandas-profiling in terms of both speed and user experience. DataPrep.EDA is open-sourced as an EDA component of DataPrep: this https URL.

# Summary. An optional shortened abstract.
summary: ""

tags:
- DataPrep
- Exploratory Data Analysis

featured: false

links:
  - name: arXiv
    url: https://arxiv.org/abs/2104.00841

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