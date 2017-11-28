## CD Cover Image Crawl
This project provide two ways to download the CD image. 

* Discogs website
* Google Image Search Engine

Prerequist:

* lxml
* requests
* urllib


#### Get information from Discogs
Discogs provide raw dataset and database API. 
##### Fetch the information through request. 
Run the code to download the image and generate search name list (max is 10000)
	cd code
	python main.py

#### Download image from Google Image 
The code will download image by the search name list (e.g., CD_list.txt) to download top "n" images.

	cd Google
	python main.py
