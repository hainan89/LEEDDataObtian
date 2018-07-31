'''
Created on 2016年10月5日

@author: Casey-NS
'''

# import xlrd;
import re;
import csv;
from src.BrowserShadowNoProxy import BrowserShadowNoProxy;
from bs4 import BeautifulSoup
from src.CRUDProcess import CRUDProcess

def obtain_proj_data():
    brw = BrowserShadowNoProxy()
    with open('../leed_projects.csv') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        record = 0
        for row in f_csv:
            profile = brw.obtain_contents(row[1])
            detail = brw.obtain_contents(row[1] + "?view=scorecard")
            parse_data(profile, detail)
            record = record + 1
            print("parse No. {0}".format(record))
            
#             break

def parse_data(profile, detial):
    p_profile = BeautifulSoup(profile, "html.parser")
    p_detail = BeautifulSoup(detial, "html.parser")
    
    ########################################################
    ## obtain profile data
    try:
        ProjName = p_profile.find("h1", class_ = "pf-title").get_text()
    except Exception as e:
        ProjName = ""
        
    try:
        Address = p_profile.find("span", itemprop="address").get_text()
    except Exception as e:
        Address = ""
        
    try:
        Description = p_profile.find("div", itemprop="description").get_text()
    except Exception as e:
        Description = ""
    
    try:    
        ProjDetails = p_profile.find("div", id = "project-details").get_text()
        str = ProjDetails.replace("\n", " ")
        s_i = str.find("Size")
        c_i = str.find("Certified")
        Size = str[s_i + 5 : c_i ]
        Certified = str[c_i + 10 :  ]
    except Exception as e:
        Size = ""
        Certified = ""
    
    try:
        Level = p_profile.find("div", class_="cert-badge").find("strong").get_text()
    except Exception as e:
        Level = ""
        
    try:    
        SystemVersion = p_profile.find("h3", class_ = "system-version").get_text()
    except Exception as e:
        SystemVersion = ""
    
    #######################################################
    ## obtain details
    scorecard = p_detail.find("div", id = "mini-scorecard")
    try:
        CertifiedScore = scorecard.find("dl", class_="points total").find_all("dd")[0].get_text()
    except Exception as e:
        CertifiedScore = 0
        
    try:
        SustainableSites = scorecard.find("dl", class_="points ss").find("span").get_text()
    except Exception as e:
        SustainableSites = ""
    
    try:
        WaterEfficiency = scorecard.find("dl", class_="points we").find("span").get_text()
    except Exception as e:
        WaterEfficiency = ""
    
    try:
        EnergyAtmosphere = scorecard.find("dl", class_="points ea").find("span").get_text()
    except Exception as e:
        EnergyAtmosphere = ""
    
    try:
        MaterialResources = scorecard.find("dl", class_="points mr").find("span").get_text()
    except Exception as e:
        MaterialResources = ""
    
    try:
        IndoorEnvironmentalQuality = scorecard.find("dl", class_="points iq").find("span").get_text()
    except Exception as e:
        IndoorEnvironmentalQuality = ""
        
    try:
        Innovation = scorecard.find("dl", class_="points id").find("span").get_text()
    except Exception as e:
        Innovation = ""
        
    try:
        RegionalPriorityCredits = scorecard.find("dl", class_="points rp").find("span").get_text()
    except Exception as e:
        RegionalPriorityCredits = ""
    
    #######################################################
    ## insert data
    insert_id = crud.insert("proj_profile", 
                "ProjName, Address, Description, Size, Certified, Level, SystemVersion, " + 
                "CertifiedScore, SustainableSites, WaterEfficiency, EnergyAtmosphere, " + 
                "MaterialResources, IndoorEnvironmentalQuality, Innovation, RegionalPriorityCredits", 
                (ProjName, Address, Description, Size, Certified, Level, SystemVersion,
                 CertifiedScore, SustainableSites, WaterEfficiency, EnergyAtmosphere,
                 MaterialResources, IndoorEnvironmentalQuality, Innovation, RegionalPriorityCredits))
    print("Insert Profile Record No. {0}".format(insert_id))
    
    #######################################################
    ## obtain detailed score
    try:
        score_list = p_detail.find("div", id = "scorecard").find_all("li")
        for one_item in score_list:
            ItemName = one_item.find_all("a")[0].get_text()
            Note = one_item.find("strong").next_sibling.encode('utf-8')
            ItemScore = one_item.find("span", class_ = "num").get_text()
            
            insert_item_id = crud.insert("item_info",
                        "ProjID, ItemName, Note, ItemScore",
                        (insert_id, ItemName, Note, ItemScore))
            print("Insert Item Info Record No. {0}".format(insert_item_id))
    except Exception as e:
        print("We currently do not have credit level data available for this project")
#


crud = CRUDProcess();
if __name__ == '__main__':
#     print("Hello LEED");
    obtain_proj_data()
# 
    crud.close()
#     str = "\n\nProject details\n\nSize\n2,885 sf\nCertified\n7 Jul 2014\n\n\n"
#     str = str.replace("\n", " ")
#     s_i = str.find("Size")
#     c_i = str.find("Certified")
#     Size = str[s_i + 5 : c_i ]
#     Certified = str[c_i + 10 :  ]
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    