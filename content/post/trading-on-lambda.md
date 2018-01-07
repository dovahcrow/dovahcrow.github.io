---
math: true
summary: >
  By sending your pdf documents to `kindle.book.converter@gmail.com` with the email address of your Amazon Kindle push service 
  as subject, you will receive a cropped version of pdf in your Kindle which has a suitable page size for reading.
categories:
  - post
tags: 
  - lambda
  - trading
  - aws
date: "2017-12-30T16:43:00-08:00"
title: "Trading on AWS Lambda"
draft: true
---

# The story

With the recent great bump on bitcoin and other altcoins, I decided to plunge myself into the market to seek some fortune. However, I admit, trading bitcoin made me fall into my unconfortable zone. The very first impression of trading in a super transient market is "uncontrollable". The market works 24/7, but I'm not an iron man. Anything that can go wrong will go wrong according to Murphy's Law, which made me always frustrate every time I wake up in the morning in these manual trading days, either missing a bump or still holding the balance during the dump. A 10% increase can be easily missed even during the time you are having a meal. 

_"That's not the correct way for trading"_ I realized. So I decided to spend my Xmas on something making me confortable, a trading bot.

I will not share my strategy here, but some experience about an amateur trading bot.

#  Lambda

Rather than the common way to build a trading bot, a self hosted server, I'm much prefer `AWS Lambda`. I'll not go for the high frequency trading direction, so the once per minute event based `Lambda` scheduler is quite enough for me. Based on my experience on the `k2pdfopt-service`(Yes, I recently moved it to AWS `Lambda` so save bucks spent on EC2), developing for `Lambda` is actually having lots of fun. Moreover, trading on `Lambda` enforces me to break down the whole bot into several components, thus actually it brings me more flexibility. I'll cover the flexibility part later. Besides the flexibility and lower cost of `Lambda`, cons include:

* Limited execution time, up to 5 minutes.
* Communication is not easy between components.
* Auto retry! This causes double orders and makes you losing money.

## Fix it!
### Limited execution time
AWS will kill your trading bot if it exceeds the time limit, dramatically decreased the reliability of the bot. 