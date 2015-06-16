#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Create time @ 2015-06-11 16:00:16

import requests
from bs4 import BeautifulSoup

class wwdc:

    def __init__(self):
        self.url = "https://developer.apple.com/videos/wwdc/2015/"
        self.sdFile = None
        self.hdFile = None

    def getPage(self, url):
        try:
            response = requests.get(url)
            return response.text
        except:
            print "Request failed"

    def getAllVideo(self, html):
        soup = BeautifulSoup(html)
        allVideosHTMLString = soup.findAll("section", attrs={"id":"all_videos"})
        allVideoHTMLList = []
        videoHtmlList = allVideosHTMLString[0].findAll('li')
        for html in videoHtmlList:
            videoHTMLURL = self.url + html.a['href']
            allVideoHTMLList.append(videoHTMLURL)
        return allVideoHTMLList

    def getDownloadURL(self, HTMLURL):
        html = self.getPage(HTMLURL)
        soup = BeautifulSoup(html)
        downloadHTML = soup.findAll("ul", attrs={"class":"smaller text-right lighter no-margin-top"})
        linksBlock = downloadHTML[0].findAll('li',attrs={"class":"inline-block"})
        SDDownloadURL = linksBlock[1].a['href']
        HDDownloadURL = linksBlock[2].a['href']
        try:
            PDFDownloadURL = linksBlock[3].a['href']
        except:
            PDFDownloadURL = ""
            print "No pdf."

        return (SDDownloadURL, HDDownloadURL, PDFDownloadURL)


    def start(self):
        html = self.getPage(self.url)
        videoHTMLURLList = self.getAllVideo(html)
        self.sdFile = open("sd.txt", "w+")
        self.hdFile = open("hd.txt", "w+")
        self.pdfFile = open("pdf.txt", "w+")
        for HTMLURL in videoHTMLURLList:
            URLs = self.getDownloadURL(HTMLURL)
            print URLs[0]
            self.sdFile.write(URLs[0] + "\n")
            self.hdFile.write(URLs[1] + "\n")
            if len(URLs[2]) > 0:
                self.pdfFile.write(URLs[2] + "\n")
        print "Done!"

wwdc = wwdc()
wwdc.start()
