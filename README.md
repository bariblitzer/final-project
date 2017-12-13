# SI 364: Homework 5

### Deadline: Monday, November 27 at 11:59 PM

### IMPORTANT NOTES:

* We will drop the "Part 1" of this assignment if it, on its own, is your lowest scoring assignment this semester. You *may not* drop the Part 2, although you may turn it in late for a deduction if you decide to do that. It's part of leading up to your final project. **The 600 points for Part 2 are required.**

* We will use "Part 2" to approve your final project idea. If we do not approve, we will offer comments so you can come up with an idea that we think will be scoped well to be doable and fulfill all the requirements!

* See below for more details. You will have some opportunities in class session(s) to work on Part 2 with your GSI and classmates' feedback.

## To Submit

Fork and clone this repository. Make edits to it as appropriate (see below), add, commit, and push them to your fork.

* **For Part 1:** Submit to Canvas a link to your fork of this repository, with edits as directed in the code file. There are comments that say `TODO` throughout the files (fewer than in HW4!). You should fix up what those comments say to make the whole application run.

* **For Part 2:** This repository also includes a markdown file with questions. You should answer all of those questions in that file, and commit the answers to the repository. We'll see these within the link to your fork.

* **For Part 2:** Also submit to canvas a file: An image (which you could use software to make, or draw on paper and scan/take a picture of it) demonstrating how data will flow through your application. See below for more instructions. Attach this to your Canvas submission.


## Instructions

**Your HW5 has two parts:**

* Completing an almost-complete Flask application to continue practicing the skills you've been learning in class. This is much shorter than HW4.

* Designing a plan and diagram for the application you will write for your final project, which you'll also have time during section to workshop and work on.

### Part 1 (400 points)

Search for all occurrences of `TODO` in the comments in the `.py` files. Fix them as directed to make the application work.

This is a lot less work than your HW4 was, and relies on some of the stuff you've already seen in HW4 and in class.

### Part 2 (600 points)

Check out the [final project requirements](https://paper.dropbox.com/doc/SI-364-Fall-2017-Final-Project-l1rUCcyM3tjvSGcjKwatZ).

The file `final_project_app_qs.md` in this repository contains questions about:

    * How data will flow through your application
    * How a user could interact with your application
    * What tables will be in your database and what relationships they will have
    * Other things!

You should edit that file to answer all of those questions.

**You should also submit a diagram showing how data will basically flow through your application.** You should consider, in your diagram:

* What data does a user enter? In what way?
* How is the data sent through the application, from the client to a view function? Which view function is it sent to?
* Is it processed with Python code in any way?
* Is it saved in any database table?
* What would keep data from being saved in a database table (think about our songs example -- where you couldn't save songs with the same title)?
* What queries are made in different view functions?
* How would a user get from one page in the application to another? A link? Submitting a form and getting redirected?

Part 2 will be graded based on being thoughtful, not necessarily stating things that will absolutely work. We will give you feedback on what you submit for your Part 2 to help you get started on the final project.
