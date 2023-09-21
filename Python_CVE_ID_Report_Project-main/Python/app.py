from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re
from py import *
app = Flask(__name__)

def fetch_cve_info(cve_id):
    cve_id = cve_id.upper()  # Convert to uppercase for consistency

    # Validate the CVE ID format
    if not re.match(r'^CVE-\d{4}-\d{4,7}$', cve_id):
        return None, None, None, None  # Return None for MITRE data

    nvd_url = f"https://nvd.nist.gov/vuln/detail/{cve_id}"
    vulmon_url = f"https://vulmon.com/vulnerabilitydetails?qid={cve_id}"

    nvd_response = requests.get(nvd_url)
    vulmon_response = requests.get(vulmon_url)

    nvd_description = None
    nvd_severity = None
    vulmon_description = None
    vulmon_severity = None
    if nvd_response.status_code == 200:
        nvd_soup = BeautifulSoup(nvd_response.content, "html.parser")
        nvd_description_element = nvd_soup.find("p", attrs={"data-testid": "vuln-description"})
        nvd_severity_element = nvd_soup.find("span", class_="severityDetail")

        nvd_description = nvd_description_element.text.strip() if nvd_description_element else "Description not found on NVD page."
        nvd_severity = nvd_severity_element.text.strip() if nvd_severity_element else "Severity not found on NVD page."

    if vulmon_response.status_code == 200:
        vulmon_soup = BeautifulSoup(vulmon_response.content, "html.parser")
        vulmon_description_element = vulmon_soup.find("p", attrs={"class": "jsdescription1"})
        vulmon_severity_element = vulmon_soup.find("div", class_="value")
        
        vulmon_description = vulmon_description_element.text.strip() if vulmon_description_element else "Description not found on NVD page."
        vulmon_severity = vulmon_severity_element.text.strip() if vulmon_severity_element else "Severity not found on NVD page."

    return nvd_description, nvd_severity, vulmon_description, vulmon_severity
def generate_report4(title,info_cve ):
    report = ""
    report += f"{title}\n"
    report += f"{info_cve}\n"
    return report
     
def generate_report3(cve_id ):
    report3 = f"CVE ID: {cve_id}\n"
     
    return report3
def generate_report(nvd_description, nvd_severity):
    report = ""
    report += f"NVD Description: {nvd_description}\n"
    report += f"NVD Severity: {nvd_severity}\n"
    return report

def generate_report2(vulmon_description, vulmon_severity):
    report2 = ""
    report2 += f"Vulmon Description: {vulmon_description}\n"
    report2 += f"Vulmon Severity: {vulmon_severity}\n"
    return report2

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        cve_id = request.form["cve_id"].replace(" ", "")  # Remove spaces
        cve_id=cve_id.upper()
        # Validate the CVE ID format
        if not re.match(r'^CVE-\d{4}-\d{4,7}$', cve_id):
            error_message = "Invalid CVE ID format. Please enter a valid CVE ID."
            return render_template("index.html", error_message=error_message)

        nvd_description, nvd_severity, vulmon_description,vulmon_severity = fetch_cve_info(cve_id)
        title,info_cve =get_info_from_links(cve_id)
        if nvd_description:
            report = generate_report(nvd_description, nvd_severity)
            report2 = generate_report2(vulmon_description,vulmon_severity)
            report3 = generate_report3(cve_id)
            report4=generate_report4(title,info_cve)

            return render_template("report.html", report=report,report2=report2,report3=report3,report4=report4)
        
    return render_template("index.html")

if __name__ == "__main__":
   
    # Scrape special links for the specified CVE ID
   
    app.run(debug=True)
