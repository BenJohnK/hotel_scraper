# hotel_scraper

A scraper developed using python scrapy framework to scrape hotel details from www.booking.com  

Working:

This scraper takes input of hotel name, check in date and checkout date. Then the scraper will collect the first lisitng page of hotels related to the input hotel name from www.booking.com. From the list of suggested hotels for the input hotel name, the first hotel will be selected as the most matched hotel for the input hotel name and details of that hotel is scraped in the next request to that hotel url and saved against the input hotel name and dates.

Please follow these steps to setup the project.  
1) clone the project to your local machine.  
2) inside the root directory of the project folder run the command python3 -m venv myenv to create a new python virtual environment  
3) activate the virtual environment by running source myenv/bin/activate  
4) install the required libraries by running pip install -r requirements.txt
5) input values for hotel name, check in date and check out date can be given inside the file called input_hotel_names.csv.
6) multiple hotel names and dates can be provided as row by row in the input csv file to collect multiple hotels details in one go.
7) Finally, run the spider using the command scrapy crawl main
8) output will be saved to outputs.csv where we can see all the scraped data of hotels that we given as input.

Thank You.
