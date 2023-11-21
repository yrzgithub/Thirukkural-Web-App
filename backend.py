from thirukkural import Kural
from os.path import isfile
from pickle import load,dump
from flask import *
from datetime import datetime,timedelta


data_path = "data/data_file"
key_lastly_opened_aram = "lastly_opened_aram"
key_lastly_opened_porul = "lastly_opened_porul"
key_lastly_opened_inbam = "lastly_opened_inbam"

key_adigaram_ta = "adigaram_ta"
key_adigaram_en = "adigaram_en"
key_adigaram_no = "adigaram_no"
key_kural_no = "kural_no"
key_paal_no = "paal_no"
key_paal_ta = "paal_ta"
key_paal_en = "paal_en"
key_kural_ta = "kural_ta"
key_kural_en = "kural_en"
key_paapaya = "paapaya"
key_english_meaning = "english_meaning"
key_varadarasan = "varadarasan"

start = 40
todays_kural = start
tot_aram = 38
tot_porul = 70
tot_inbam = 25 

now = datetime.now()

app = Flask(__name__)


if isfile(data_path):
    with open(data_path,"rb") as file:
        data = load(file)
        file.close()

    todays_kural_aram =  timedelta(now,data[key_lastly_opened_aram]).days + 1 
    todays_kural_porul = timedelta(now,data[key_lastly_opened_porul]).days + 1
    todays_kural_inbam = timedelta(now,data[key_lastly_opened_inbam]).days + 1

    if todays_kural_aram>tot_aram:
        data[key_lastly_opened_aram] = day_only
        todays_kural_aram = 1

    if todays_kural_porul>tot_porul:
        data[key_lastly_opened_porul] = day_only
        todays_kural_porul = 1

    if todays_kural_inbam>tot_inbam:
        data[key_lastly_opened_inbam] = day_only
        todays_kural_inbam = 1

else:
    data = {key_lastly_opened_aram:day_only,key_lastly_opened_porul:day_only,key_lastly_opened_inbam:day_only}
    with open(data_path,"wb") as file:
        dump(data,file)
        file.close()

    todays_kural_aram = todays_kural_porul = todays_kural_inbam = start



def get_kural_data(kural_no):
    kural = Kural(kural_no)

    tamil_adigaram = kural.adigaaram_ta
    english_adigaram = kural.adigaaram_en
    adigaram_no = kural.adigaaram_no
    kural_no = kural.kuralNo
    paal_no = kural.paal_no
    paal_ta = kural.paal_ta
    paal_en = kural.paal_en
    kural_ta = kural.kural_ta.replace("\n","\n   ")
    kural_en = kural.kural_en
    english_meaning = kural.en_meaning
    paapaya = kural.paapaya
    varadarasan = kural.varadarasan

    return {key_adigaram_ta:tamil_adigaram,key_adigaram_en:english_adigaram,key_adigaram_no:adigaram_no,key_kural_no:kural_no,
            key_paal_no:paal_no,key_paal_ta:paal_ta,key_english_meaning:english_meaning,key_paal_en:paal_en,key_kural_ta:kural_ta,key_kural_en:kural_en,key_paapaya:paapaya,key_varadarasan:varadarasan}


def get_page(next,kural_number):
    print("Kural no",kural_number)
    thirukural_data = get_kural_data(kural_number)

    paal_ta = thirukural_data[key_paal_ta]
    paal_en = thirukural_data[key_paal_en]
    paal_no = thirukural_data[key_paal_no]

    adigaaram_ta = thirukural_data[key_adigaram_ta]
    adigaaram_en = thirukural_data[key_adigaram_en]
    adigaaram_no = thirukural_data[key_adigaram_no]

    no = thirukural_data[key_kural_no]
    Kural_ta = thirukural_data[key_kural_ta]
    kural_en = thirukural_data[key_kural_en]

    paapaya = thirukural_data[key_paapaya]
    varadarasan = thirukural_data[key_varadarasan]

    english_meaning = thirukural_data[key_english_meaning]

    return render_template("home.html",en_meaning=english_meaning,paal_data = f"{paal_no}. {paal_ta} ({paal_en})",adigaram_data = f"{adigaaram_no}. {adigaaram_ta} ({adigaaram_en})",kural_ta =f"{no}. {Kural_ta}",kural_en = kural_en,varatharasan = varadarasan,paapaya = paapaya,next=next)


@app.route("/")
def home():
    return redirect(url_for("aram"))


@app.route("/aram")
def aram():
    print("Kural No : ",todays_kural_aram)
    return get_page("porul",todays_kural_aram)


@app.route("/porul")
def porul():
    print("Kural No : ",todays_kural_porul)
    kural_no = tot_aram * 10 + todays_kural_porul
    return get_page("inbam",kural_no)


@app.route("/inbam")
def inbam():
    print("Kural No : ",todays_kural_inbam)
    kural_no = tot_aram * 10 + tot_porul * 10 + todays_kural_inbam
    return get_page("/",kural_no)



app.run(debug=True)