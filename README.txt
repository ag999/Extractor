I have written the program in Python 3.4.3. In this program, I use regular expressions (regex) to find and extract the handles. I chose to use regex because I would have to find multiple instances of the handles on a page and this would give better performance for that. It also increased the readability and makes it easier to understand as to what is happening. I started with a basic regex pattern and then as I visited more pages and saw something is not working as it should, I updated the regex. I am still doing that to make it more efficient and accurate. I make my regex using https://regex101.com/r/sH1hX1/2. It is essentially like the teaching phase of a machine learning program, except here I do it manually. I read the page using the module requests and catch errors using the same. Requests is not a built in library and needs to be installed seperately. Currently, I catch the following as errors: bad URLs, redirect requests, timeout (set as 10). Once the page is read, the regex pattern works its magic. It finds all the handles on the page and I get a list of all the handles present. Now I have to choose which one is correct. I have made a dictionary, called redundant, of some words which tend to come up as handles, as their format is the same as that of the page ids. Dictionary so that the lookup time is O(1). This is also something that I keep updating as and when I find some of these through trying different websites. I have gone through a lot of pages to find these and am still going through more and updating this. The hierarchy I follow to find the correct handle is as follows:
1) If only one handle is found
2) See if complete match with the domain name
3) See if it contains the domain name
4) See if it contains first half of the domain name
5) See if it contains last half of the domain name
6) Return either the first or the last instance found
7) I make sure to check that the found handle is not present in the redundant
I have come up with the above hierarchy after visiting many pages. I think it could be made better, especially, the 6) part where I just return the first or the last instance. I chose that because in most of the pages that is where the handle was present.
The above procedure is for the twitter handle and facebook page id. I have not found any efficient way of checking the app ids.
Once the handles are returned, I print out the result in JSON format.
Things I am still working on:
1) Making the regex more accurate and efficient
2) Marking some words as redundant (they aren't the handle, but just have a similar URL format which the regex accepts)
3) Finding a better set of rules (I think I would be able to do this better after learning some Machine Learning techniques next semester)

How to use:
You would need to install an external Python library called requests if you don't have it already.
To install the library you would need pip and the command for installing this library is `pip3 install requests`
Once you have installed this library, follow the following steps to run the program.
1) Navigate to the directory where the folder for this program is and open Python 3.4.3
2) Import the module in the working environment that runs Python 3.4.3 (import extractor)
3) Call the main function in the module and pass in the URL as the argument (something like extractor.main("https://sampleurl.com"))
