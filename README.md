SI 364 Fall 2017: Final Project

My application creates personal movie collections for the user. The user is asked to input 3 of their favorite actors and a comma-separated list of the genres of their choice.

IMPORTANT!!! When typing in genres, the user only has the genre options of: comedy, drama, classics, thriller.

The app then displays a list of movies (hyperlinks) that contain these actors and genre types. The user can then click on the link of a movie --> which will take them to that movie page that contains an image of the film and a long description from the iTunes API. The user then has the option to click the button 'Add to my Collection', which not only takes the user to their collection list, but it sends the user an email of their current list as well.


Run the application in terminal with --> python final.py runserver

When the user creates a new account their information will be submitted into the 'users' table and the movie information will be stored under that user's id.