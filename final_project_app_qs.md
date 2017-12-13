# SI 364 - Final Project questions

## Overall

* **What's a one-two sentence description of what your app will do?**
--> My application will basically put together movie collections based on user preferences. 


## The Data

* **What data will your app use? From where will you get it? (e.g. scraping a site? what site? -- careful not to run it too much. An API? Which API?)**
--> My app will take data from the iTunes API (specifically movie/actor/director data)

* **What data will a user need to enter into a form?**
--> The user will need to enter data regarding their favorite actors, genres of movies and all-time directors.

* **How many fields will your form have? What's an example of some data user might enter into it?**
--> There will be 4 fields in my form. An example of some data that a user might enter in it would be their top 5 favorite actors, a checklist of genres they enjoy, etc.

* **After a user enters data into the form, what happens? Does that data help a user search for more data? Does that data get saved in a database? Does that determine what already-saved data the user should see?**
--> Once a user enters data into the form, another form will be posted that takes the artists and returns a long list of movies (that those actors starred in/that line up with the genres they previously picked)

* **What models will you have in your application?**
--> Film collections, movies, actors, genres, directors

* **What fields will each model have?**
--> StringFields

* **What uniqueness constraints will there be on each table? (e.g. can't add a song with the same title as an existing song)**
--> Can't add a movie with the same name as an existing movie (the rest can be)

* **What relationships will exist between the tables? What's a 1:many relationship between? What about a many:many relationship?**
--> 1:many relationship will be movie to actors, director to movies
--> many:many relationship will be movies to genres, actors to movies

* **How many get_or_create functions will you need? In what order will you invoke them? Which one will need to invoke at least one of the others?**
--> 3 get_or_create functions will be needed. The first function will be to create a list of movies with specified actors and directors. The second function will sort through that data by genre. The third function will invoke both of the other functions to create a collection.

## The Pages

* **How many pages (routes) will your application have?**
--> My application will have 4 routes

* **How many different views will a user be able to see, NOT counting errors?**
--> The user will see 5 pages

* **Basically, what will a user see on each page / at each route? Will it change depending on something else -- e.g. they see a form if they haven't submitted anything, but they see a list of things if they have?**
- First page: welcome page
- Second page: questions about actors and directors
- Third page: choice of genres
- Fourth page: a list of movie collections based on genres

## Extras

* **Why might your application send email?**
- Send the uesr an email of their final movie collection list to use in the future

* **If you plan to have user accounts, what information will be specific to a user account? What can you only see if you're logged in? What will you see if you're not logged in -- anything?**

* **What are your biggest concerns about the process of building this application?**
- Being able to correctly sort through the data of movies and genres using the iTunes API is definitely a concern of mine
