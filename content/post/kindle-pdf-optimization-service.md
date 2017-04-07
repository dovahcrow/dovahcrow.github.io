---
math: true
summary: >
  By sending your pdf documents to `kindle.book.converter@gmail.com` with the email address of your amazon kindle push service 
  as subject, you will receive a cropped version of pdf in your kindle which has a suitable page size for reading.
categories:
  - post
tags: 
  - kindle
  - public service
date: "2016-12-22T17:36:19+08:00"
title: "Kindle PDF Optimization Service"
draft: false
---

I'm fond of reading academic things on my kindle, however, most academic papers are not
designed to be read on a 6 inch size screen, let alone those with two columns format. 

I took two days writing a service and now things goes easy. You can just send your pdf 
to `kindle.book.converter@gmail.com` with your `amazon kindle push service email address` 
as subject, then a cropped version of your book will be pushed to your kindle automatically. 
Notice that the email address you used to send email to `kindle.book.converter@gmail.com` 
should also have permissions to push books to your kindle directly.

A caveat is that if your 
book contains too much pages, the mailer may reject sending the attachment for its huge size, 
but you can enter a subset of pages (e.g. `1-9,13,209-`) in the email content to shrink the result file size.
The input format is:

  * Single Page - e.g. `1`
  * Some Pages - e.g. `5-9`
  * Page Since - e.g. `10-`
  
And use comma `,` to combine the page selections, e.g. `1,5-9,10-`. There should not be any spaces inside the page selection.

Basically this service will crop your book into a kindle readable format on server 
and send it pretending it is you sending the book by mocking the email address.

Be carefull, you should not send classified documents to this address! Although I will delete them in place on the server, the document will exist in
gmail trash for several days until google purge the trash bin automatically. And if something goes wrong, I may replay attachments in the trash bin to debug.
So please DON'T SEND CLASSIFIED or PRIVATE DOCUMENTS to me in order to keep me away from legal issue.

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