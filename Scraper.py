import requests
from bs4 import BeautifulSoup as bs
import csv

def Scrape_Html(link):
    HEADERS=({'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36'})
    html_file=requests.get('https://www.amazon.in'+link,headers=HEADERS).text
    return html_file

def scrape_productdetails(item):
    product_details=item.find('div',{'id':'detailBullets_feature_div'})
    if product_details==None:
        product_details=item.find('div',{'id':'prodDetails'})
    else:
        pass
    product_details=product_details.text;
    l=product_details.replace('\n','').replace(':','').replace('\u200f','').replace('\u200e','')
    count=0;
    s=''
    cleaned_data=[]
    for i in l:
        if i==' ':
            count+=1;
        else:
            s=s+i;
            count=0;
        if count==2:
            if s!='':
                cleaned_data.append(s);
            s=''
            count=0;

    i=0;
    print(cleaned_data)
    asin_mfg={}
    count1=0;
    count2=0;
    for detail in cleaned_data:
        if detail.lower() == 'asin':
            asin_mfg[detail.lower()]=cleaned_data[i+1];
            count1=1;
        elif detail.lower() == 'manufacturer':
            asin_mfg[detail.lower()]=cleaned_data[i+1];
            count2=1;

        if count1==1 and count2==1:
            break;
        i+=1;
    try:
        asin_mfg['asin'];
    except:
        asin_mfg['asin']='None';
        
    try:
        asin_mfg['manufacturer'];
    except:
        asin_mfg['manufacturer']='None';
    return asin_mfg

def scrape_productDescription(item):
    product_description=item.find('div',{'id':'productDescription_feature_div'})
    
    if product_description==None:
        try:
            product_description=item.find('div',{'id':'aplus'})
        except:
            return None;
    else:
        pass;    
    if product_description.text=='':
        return None;
    else:
        return product_description.text.replace('Product description','')
    
        #print(product_description.text)
        
def main():
    scraper=bs(Scrape_Html('/s?k=bags&page=2&crid=2M096C61O4MLT&qid=1679421216&sprefix=ba%2Caps%2C283&ref=sr_pg_1'),'lxml');
    data = [
        ['ProductName','ProductUrl','Price','Review','Ratings','Description','Asin','Manufacturer'],
    ]
    products=scraper.find_all('div',{"data-component-type":"s-search-result"})

    for product in products:
        productDetails_collection=[]
        product_heading=heading=product.find('h2')#jj heading extracted 
        product_url=heading.find('a').get('href'); #url extracted
        product_rating=product.find('span',{"class":"a-size-base"})
        product_price=product.find('span',{'class':'a-price'})
        reviewsParent=product.find('div',{'class':'a-spacing-top-micro'})
        parent_reviews=reviewsParent.find('span',{'class':'s-underline-text'})
        productDetails_collection.append(heading.text)
        productDetails_collection.append('www.amazon.in'+product_url)
        productDetails_collection.append('₹'+product_price.text.replace('₹',' ').split()[0]);
        productDetails_collection.append(parent_reviews.text.replace('-',''))
        productDetails_collection.append(product_rating.text)
        
        scraper2=bs(Scrape_Html(product_url),'html.parser')
        item=scraper2.find('body')
        productDetails_collection.append(scrape_productDescription(item))
        asin_mfg=scrape_productdetails(item);
        productDetails_collection.append(asin_mfg['asin'])
        productDetails_collection.append(asin_mfg['manufacturer'])
        data.append(productDetails_collection)

    with open('example.csv', 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)

        # Write the data to the CSV file
        writer.writerows(data)
    print(' Done :) ');

main();