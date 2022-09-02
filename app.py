from bs4 import BeautifulSoup as bs
import requests
from flask import Flask,request,render_template
from flask_cors import cross_origin


app=Flask(__name__)

@app.route("/",methods=['GET']) #route to display Homepage
@cross_origin()
def homepage():
    return render_template('index.html')

@app.route("/review",methods=['POST','GET'])
@cross_origin()
def index():
    if request.method=='POST':
        try:
            searchString=request.form['content'].replace(' ',"")
            flipKart_url=f"https://www.flipkart.com/search?q={searchString}"
            r=requests.get(flipKart_url)
            htmlpage=r.content

            soup=bs(htmlpage,"html.parser")
            results=soup.find_all('div',{'class':'_1AtVbE col-12-12'})
            del results[0:2]
            res=results

            filename = searchString + ".csv"
            fw = open(filename, "w")
            headers = "Device, Price, Rating,Features, LINK \n"
            fw.write(headers)



            reviews=[]
            for item in res:
                try:
                    Device = item.find('div', {'class': '_4rR01T'}).text
                except:
                    Device='No Device'

                try:
                    Price= item.find('div', {'class': '_30jeq3 _1_WHN1'}).text
                except:
                    Price='not available'

                try:
                    Rating = item.find('div', {'class': '_3LWZlK'}).text
                except:
                    Rating="No Rating"

                try:
                    Features = item.find('ul', {'class': '_1xgFaf'}).text
                except:
                    Features='Coming soon'
                try:
                    link = "https://www.flipkart.com" + item.find('a')['href']
                except:
                    link='NAN'


                mydict = {"Product": Device,"Price": Price, "Rating": Rating,
                          "Features": Features ,"link":link}
                reviews.append(mydict)

            return render_template('results.html', reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'
    # return render_template('results.html')

    else:
        return render_template('index.html')

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app.run(debug=True,port=5002)

