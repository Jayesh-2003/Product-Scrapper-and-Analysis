import requests
from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from scraper_api import ScraperAPIClient

def retrieve_products():
    urls = url_entry.get("1.0", tk.END).strip().split('\n')

  
    products = []

    for url in urls:
        
     
        
        client = ScraperAPIClient('bed738977fa4db0c76849c5e996de377')  
        response = client.get(url)
        content = response.content
        
        soup = BeautifulSoup(content, 'html.parser')
        
       
        try:
            title = soup.find('span', {'id': 'productTitle'}).get_text().strip()
            
        except:
            title = 'Not_found'

     
        try:
            price = soup.find('span', {'class': 'a-price-whole'}).get_text().replace(',', '').strip()
        except:
            price = 'Not_found'

       
        try:
            feature_list = soup.find('div', {'id': 'feature-bullets'}).find_all('span', {'class': 'a-list-item'})
            features = ''
            for feature in feature_list:
                features += feature.get_text().strip() + '\n'
        except:
            features = 'Not_found'

        
        try:
            rating = soup.find('span', {'class': 'a-icon-alt'}).get_text().strip().split()[0]
        except:
            rating = 'Not_found'

        
        products.append([title, price, features, rating,url])

    
    file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    if file_path:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file,delimiter=' ')
            writer.writerow(['Title', 'Price', 'Features', 'Rating','URL'])
            for product in products:
                writer.writerow(product)

        
        df = pd.read_csv(file_path, sep=' ')

        window = tk.Toplevel()
        window.title('Product Information')

        # Create a Canvas to hold the table
        canvas = tk.Canvas(window)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a Scrollbar for vertical scrolling
        scrollbar_y = ttk.Scrollbar(window, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a Scrollbar for horizontal scrolling
        scrollbar_x = ttk.Scrollbar(window, orient=tk.HORIZONTAL, command=canvas.xview)
        scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

         # Configure the Canvas to work with the Scrollbars
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        canvas.bind('<Configure>', lambda event: canvas.configure(scrollregion=canvas.bbox('all')))

        # Create a Frame inside the Canvas to hold the table
        table_frame = tk.Frame(canvas)
        canvas.create_window((0,0), window=table_frame, anchor='w')

        # Display column headings
        tk.Label(table_frame, text="Title", borderwidth=1, relief='solid', width=150).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(table_frame, text="Price", borderwidth=1, relief='solid', width=10).grid(row=0, column=1, padx=5, pady=5)
        tk.Label(table_frame, text="Features", borderwidth=1, relief='solid', width=60).grid(row=0, column=2, padx=5, pady=5)
        tk.Label(table_frame, text="Rating", borderwidth=1, relief='solid', width=10).grid(row=0, column=3, padx=5, pady=5)

        # Display product information in rows
        for i in range(len(df)):
            title_label = tk.Label(table_frame, text=df.iloc[i, 0], borderwidth=1, relief='solid', width=150)
            title_label.grid(row=i+1, column=0, padx=5, pady=5)
            price_label = tk.Label(table_frame, text=df.iloc[i, 1], borderwidth=1, relief='solid', width=10)
            price_label.grid(row=i+1, column=1, padx=5, pady=5)
            features_label = tk.Label(table_frame, text=df.iloc[i, 2], borderwidth=1, relief='solid', width=150)
            features_label.grid(row=i+1, column=2, padx=5, pady=5)
            rating_label = tk.Label(table_frame, text=df.iloc[i, 3], borderwidth=1, relief='solid', width=10)
            rating_label.grid(row=i+1, column=3, padx=5, pady=5)



        # Update the Scrollbars
        scrollbar_y.config(command=canvas.yview)
        scrollbar_x.config(command=canvas.xview)
        # Update scrollregion to include the full width of the table frame
        table_frame.update_idletasks()
        canvas.configure(scrollregion=(0, 0, table_frame.winfo_width(), table_frame.winfo_height()))

        titles=df['Title'].tolist()
        prices=df['Price'].tolist()
            
        for i in range(0, len(prices)):
            prices[i] = float(prices[i])
        short_titles=[]
        for title in titles:
            short_title=title[:15]
            short_titles.append(short_title)
        # fig, plt=plt.subplots()
        plt.bar(short_titles,prices,width=0.1)
        plt.xlabel("Title")
        plt.ylabel("Prices")
        plt.title("Comparision")
        # plt.yticks(20000,20100,20200,20300,20400,20500,20600)
        plt.show()
        window.mainloop()



root = tk.Tk()
root.configure(bg='#47494D')
root.title('Product Price Comparison')

url_label = tk.Label(root, text='Product URLs:',fg="white",bg="#47494D")
url_label.pack()

url_entry = tk.Text(root, width=50, height=10,bg="#47494D",fg="#FFFFFF")
url_entry.pack()

retrieve_button = tk.Button(root, text='Retrieve Product Information', command=retrieve_products, fg="white",bg="blue",activebackground="#19D41E")
retrieve_button.pack()

root.mainloop()