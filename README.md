# caprae_application
IndiReach!

I was extremely curious about this opportunity so naturally the first thing when I navigated to https://www.saasquatchleads.com was to test out its utilities and extract useful information for leads for myself. While doing so, I noticed how USA and Canada-centric it currently is. It uses BBB to rate businesses which only lists USA and Canada based enterprises. After reading the doc for the submission, I decided at once to choose the “Quality” approach and to extend the functionalities of Saasquatch leads to India (my country!). At first I tried finding the source code for this web application as I thought the basic idea of the assignment was to create a pull request that layered my functionality on top of the existing application. Upon not finding the source code, I took to creating my own little application for demonstrating my approach. It can easily be integrated with the main app still!

I generated a web scraper for Naukri.com, India’s leading online job recruitment portal. Then I followed the basic flow of Saasquatch leads and added a “select few job and enhance them” option. Upon “enhancing” a job, lead, my code attempts at finding the home page of the company offering that listing as well as a valid mail id to contact the same. The mail validation process was an interesting one to implement. I used SMTP verification to validate email addresses generated through pattern-based heuristics, which were based and built on common naming convention.

Choosing the quality first track was my original approach because I assessed the shortcomings of this platform. I believe it has potential; what it’s trying to do can be done much better with algorithmic improvements and fine tuning!

I had many more ideas such as adding a mail template and allowing mailing the validated mail ids, but considering the 5 hour cap, I implemented little of what I could come up with and cut corners in doing so.

Thank you for this opportunity, I got the chance to learn a lot from this! :)
