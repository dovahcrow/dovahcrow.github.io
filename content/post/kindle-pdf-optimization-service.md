---
math: true
summary: >
  By sending your pdf documents to `kindle.book.converter@gmail.com` with the email address of your Amazon Kindle push service 
  as subject, you will receive a cropped version of pdf in your Kindle which has a suitable page size for reading.
categories:
  - post
tags: 
  - kindle
  - public service
date: "2016-12-22T17:36:19+08:00"
title: "Kindle PDF Optimization Service"
draft: false
---
# Update:
  Due to lack of funding, I decided to move it to another service provider which brings in new constraints to this service:
  
  * Total file size for a single email may not be larger than 6 MB. So if you have multiple files to convert, please send them in separate emails 
  * File should be finished converting within 5 min, which means your file cannot have many pages. So if you want to convert a whole book, please cut them into small batches. In principle, this service suits most for paper reading.
  
# What it is?

I'm fond of reading academic things on my Kindle, however, most academic papers are not
designed to be read on a 6-inch size screen, let alone those with two columns format. 

I took two days writing a service and now things go easy. You can just send your pdf 
to `kindle.book.converter@gmail.com` with your `Amazon Kindle push service email address` 
as subject, then a cropped version of your book will be pushed to your Kindle automatically. 
Notice that the email address you used to send email to `kindle.book.converter@gmail.com` 
should also have permissions to push books to your Kindle directly.

Basically, this service will crop your book into a Kindle-readable format on server 
and send it pretending it is you sending the book by mocking the email address.

# Page selection if file too large

One thing is that if the book contains too many pages, the mailer may reject sending the attachment for its huge size, 
but you can enter a subset of pages (e.g. `1-9,13,209-`) in the email content to shrink the result file size.
The input format is:

  * Single Page - e.g. `1`
  * Some Pages - e.g. `5-9`
  * Page Since - e.g. `10-`
  
And use comma `,` to combine the page selections, e.g. `1,5-9,10-`, with a prepending `# ` to indicate it's a page selection command. There should not be any spaces inside the page selection.

# Additional params

Currently, this service supports params including page selection and raw k2pdfopt params by writing them in mail body. Only one
PDF file should be attached if params are used.

Detailed grammar:

* Prepending `#` with a `space` to do page selection, e.g. `# 1,5-9,10-` (from the above example).
* Prepending `@` with a `space` to do pass raw params to k2pdfopt, e.g. `@ -p 1,5-9,10-` is same as `# 1,5-9,10-` if you know the param `-p` is page selection for `k2pdfopt`, resulting in `k2pdfopt -p 1,5-9,10- -o <filename>_converted.pdf <filename>` be called (if you know how to use `k2pdfopt`, then you will definetely understand this. Otherwise, `# ` is enough for you).

# Caveat

Be careful, you should not send classified documents to this address! Although I will delete them in place on the server, the document will exist in
Gmail trash for several days until Google purge the trash bin automatically. And if something goes wrong, I may replay attachments in the trash bin to debug.
So please **DON'T SEND CLASSIFIED** or **PRIVATE DOCUMENTS** to me in order to keep me away from legal issues.

# Thanks

Great thanks to [willus](http://www.willus.com/) who provided 
[this excellent tool](http://www.willus.com/k2pdfopt/) to produce 
the kindle readable version of pdf.

<center>
    <hr/>
    <p> Do you like the service? </p>
       <p> It costs me several bucks to maintain the server and email sending service </p>
    <p> I'm really <strong>appreciate</strong> it if you can offer me a cup of coffee :)</p>
    <form action="https://www.paypal.com/cgi-bin/webscr" method="post" target="_top">
        <input type="hidden" name="cmd" value="_s-xclick" />
        <input type="hidden" name="hosted_button_id" value="LKM2L7LDMU6ZS" />
        <input type="image" src="https://www.paypal.com/en_US/i/btn/btn_donate_LG.gif" border="0" name="submit" title="Offer me a coffee with Paypal :)" alt="Offer me a coffee" />
        <img alt="" border="0" src="https://www.paypal.com/en_US/i/scr/pixel.gif" width="1" height="1" style="margin-top: 0; margin-bottom: 0;"/>
    </form>
    <p style="margin-top: 0; margin-bottom: 0;"> -- OR -- </p>
    <h3 style="margin-top: 0; margin-bottom: 0;"> Bitcoin </h3>
    <img ng-src="https://chart.googleapis.com/chart?chs=150x150&amp;cht=qr&amp;chl=1DyAXYcQy4HNWu83vRho1b8b15zqKn9qd6&amp;choe=UTF-8" ng-show="showqr" src="https://chart.googleapis.com/chart?chs=150x150&amp;cht=qr&amp;chl=1DyAXYcQy4HNWu83vRho1b8b15zqKn9qd6&amp;choe=UTF-8" style="margin-top: 0; margin-bottom: 0;">
    <p style="margin-top: 0; margin-bottom: 0;"> 1DyAXYcQy4HNWu83vRho1b8b15zqKn9qd6 </p>
</center>