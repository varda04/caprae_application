from flask import Flask, render_template, request
from scraper import scrape_naukri_jobs, get_company_website, scrape_contact_info
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
jobs_info = []
@app.route('/', methods=['GET', 'POST'])
def index():
    global jobs_info
    jobs = []
    keyword = ''
    location = ''
    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip()
        location = request.form.get('location', '').strip()
        if keyword and location:
            jobs = scrape_naukri_jobs(keyword, location, max_pages=3)
            jobs_info= jobs
    return render_template('index.html', jobs=jobs, keyword=keyword, location=location)

def build_enriched_job_info(company, location):
    domain = get_company_website(company, location)
    info = scrape_contact_info(domain)
    return {
        'company': company,
        'location': location,
        'email': info.get('email'),
        'website': domain
    }

from concurrent.futures import ThreadPoolExecutor, as_completed

@app.route("/know_more_bulk", methods=["POST"])
def know_more_bulk():
    selected = request.form.getlist("selected_jobs")
    domain_cache = {}
    detailed_info = []

    def process_entry(entry):
        try:
            company, location = entry.split("||")
            domain = get_company_website(company, location)
            if not domain:
                return {}
            if domain in domain_cache:
                info = domain_cache[domain]
            else:
                info = scrape_contact_info(domain)
                domain_cache[domain] = info
            return {
                "company": company,
                "location": location,
                "email": info.get("email"),
                "website": domain,
            }
        except Exception as e:
            print(f"Error processing entry '{entry}':", e)
            return {}

    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_entry, entry) for entry in selected]
        for future in as_completed(futures):
            detailed_info.append(future.result())

    return render_template("know_more.html", jobs=detailed_info)



if __name__ == '__main__':
    app.run(debug=True)