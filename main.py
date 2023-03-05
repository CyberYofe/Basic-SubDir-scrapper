import tkinter as tk
import requests
from bs4 import BeautifulSoup
import re

class SubdirScraper:
    def __init__(self, master):
        self.master = master
        master.title("Subdirectory Scraper")

        self.url_label = tk.Label(master, text="Enter URL:")
        self.url_label.pack()
        self.url_label = tk.Label(master, text="Example(https://discord.com)")
        self.url_label.pack()
        self.url_entry = tk.Entry(master, width=50)
        self.url_entry.pack()

        self.scrape_button = tk.Button(master, text="Scrape Subdirectories", command=self.scrape_subdirs)
        self.scrape_button.pack()

        self.subdir_frame = tk.Frame(master)
        self.subdir_text = tk.Text(self.subdir_frame, wrap=tk.WORD)
        self.subdir_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def scrape_subdirs(self):
        url = self.url_entry.get()

        # Make a GET request to the URL
        response = requests.get(url)

        # Use BeautifulSoup to parse the HTML content of the response
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the links on the page
        links = soup.find_all('a')

        # Create a list to store the subdirectories
        subdirs = []

        # Loop through each link and check if it is a subdirectory
        for link in links:
            href = link.get('href')
            if href is not None and re.match('^/', href):
                subdirs.append(href)

        # Display the list of subdirectories
        if subdirs:
            self.subdir_frame.pack()
            self.subdir_text.delete('1.0', tk.END)
            for subdir in subdirs:
                self.subdir_text.insert(tk.END, subdir+'\n')
            self.subdir_text.config(state=tk.DISABLED)
        else:
            tk.Label(self.master, text="No subdirectories found.").pack()

    def copy_text(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.subdir_text.get('1.0', tk.END))

root = tk.Tk()
scraper = SubdirScraper(root)
copy_button = tk.Button(root, text="Copy Subdirectories to Clipboard", command=scraper.copy_text)
copy_button.pack()
root.mainloop()
