---
title: "ConnectorX: Accelerating Data Loading From Databases to Dataframes"
authors:
  - Xiaoying Wang
  - Weiyuan Wu
  - Jinze Wu
  - Yizhou Chen
  - Nick Zrymiak
  - Changbo Qu
  - Lampros Flokas
  - George Chow
  - Jiannan Wang
  - Tianzheng Wang
  - Eugene Wu
  - Qingqing Zhou

author_notes:
- "Equal contribution"
- "Equal contribution"

date: "2022-02-01"
doi: ""

# Schedule page publish date (NOT publication's date).
publishDate: "2022-02-01"

# Publication type.
# Legend: 0 = Uncategorized; 1 = Conference paper; 2 = Journal article;
# 3 = Preprint / Working Paper; 4 = Report; 5 = Book; 6 = Book section;
# 7 = Thesis; 8 = Patent
publication_types: ["1"]

# Publication name and optional abbreviated publication name.
# publication: "VLDB 2021"
# publication_short: "VLDB 2021"

abstract: >
  Data is often stored in a database management system (DBMS) but dataframe libraries are widely used among data scientists. An im- portant but challenging problem is how to bridge the gap between databases and dataframes. To solve this problem, we present Con- nectorX, a client library that enables fast and memory-efficient data loading from various databases (e.g.,PostgreSQL, MySQL, SQLite, SQLServer, Oracle) to different dataframes (e.g., Pandas, PyArrow, Modin, Dask, and Polars). We first investigate why the loading pro- cess is slow and why it consumes large memory. We surprisingly find that the main overhead comes from the client-side rather than query execution and data transfer. We integrate several existing and new techniques to reduce the overhead and carefully design the system architecture and interface to make ConnectorX easy to extend to various databases and dataframes. Moreover, we propose server-side result partitioning that can be adopted by DBMSs in order to better support exporting data to data science tools. We conduct extensive experiments to evaluate ConnectorX and com- pare it with popular libraries. The results show that ConnectorX significantly outperforms existing solutions. ConnectorX is open sourced at: https://github.com/sfu-db/connector-x.

# Summary. An optional shortened abstract.
summary: ""

tags:
  - Data Loading

featured: false

url_pdf: files/ConnectorX.pdf

links:
  # - name: arXiv
  #   url: https://arxiv.org/pdf/2012.06743.pdf

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