"""
Generate 200 realistic B2B HVAC/climate industry CRM records
with intentionally built-in duplicates for demonstration.
"""

import pandas as pd
import random
import os

random.seed(42)

SALES_REPS = [
    "Sarah Chen", "Michael Wong", "David Liu", "Emily Tan",
    "James Lee", "Anna Zhang", "Robert Ng", "Lisa Huang"
]

INDUSTRIES = [
    "HVAC", "Manufacturing", "Construction", "Building Services",
    "Refrigeration", "Climate Technology", "Energy Solutions",
    "Property Management", "Facilities Management", "Engineering"
]

STATUSES = ["Active", "Inactive", "Prospect"]

CITIES_COUNTRIES = [
    ("Hong Kong", "Hong Kong"), ("Singapore", "Singapore"),
    ("Tokyo", "Japan"), ("Shanghai", "China"), ("Bangkok", "Thailand"),
    ("Seoul", "South Korea"), ("Taipei", "Taiwan"), ("Sydney", "Australia"),
    ("Melbourne", "Australia"), ("Kuala Lumpur", "Malaysia"),
    ("Jakarta", "Indonesia"), ("Manila", "Philippines"),
    ("Dubai", "UAE"), ("Mumbai", "India"), ("Ho Chi Minh City", "Vietnam"),
]

STREETS = [
    "123 Queen's Road Central", "456 Orchard Road", "789 Nanjing Road",
    "Unit 1201, Tower 2, Times Square", "15/F, One Pacific Place",
    "Suite 3001, ICC Tower", "8 Finance Street", "22 Des Voeux Road",
    "100 Nathan Road", "50 Raffles Place", "12 Marina Boulevard",
    "Block A, Science Park", "Unit 501, Cyberport 3", "88 Queensway",
    "Level 18, Central Plaza", "25 Canton Road", "10 Harbour Road",
    "33 Hysan Avenue", "1 Austin Road West", "200 Hennessy Road",
]


def _rand_phone(city):
    """Generate a random phone number with formatting variations."""
    codes = {
        "Hong Kong": "852", "Singapore": "65", "Tokyo": "81",
        "Shanghai": "86", "Bangkok": "66", "Seoul": "82",
        "Taipei": "886", "Sydney": "61", "Melbourne": "61",
        "Kuala Lumpur": "60", "Jakarta": "62", "Manila": "63",
        "Dubai": "971", "Mumbai": "91", "Ho Chi Minh City": "84",
    }
    code = codes.get(city, "852")
    number = "".join([str(random.randint(0, 9)) for _ in range(8)])
    fmt = random.choice(["plus_space", "dash", "paren", "plain"])
    if fmt == "plus_space":
        return f"+{code} {number[:4]} {number[4:]}"
    elif fmt == "dash":
        return f"{code}-{number[:4]}{number[4:]}"
    elif fmt == "paren":
        return f"({code}) {number[:4]}-{number[4:]}"
    else:
        return f"+{code}{number}"


def _rand_date(year_range=(2022, 2025)):
    """Generate random date in mixed formats."""
    y = random.randint(*year_range)
    m = random.randint(1, 12)
    d = random.randint(1, 28)
    fmt = random.choice(["iso", "slash", "text"])
    if fmt == "iso":
        return f"{y}-{m:02d}-{d:02d}"
    elif fmt == "slash":
        return f"{d:02d}/{m:02d}/{y}"
    else:
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        return f"{months[m-1]} {d}, {y}"


def _rand_revenue():
    return random.choice([
        500000, 750000, 1000000, 1500000, 2000000, 3000000,
        5000000, 8000000, 10000000, 15000000, 25000000, 50000000,
        75000000, 100000000, 250000000, 500000000, None
    ])


def _make_record(rid, company, contact, email, phone, address, city,
                 country, website, industry=None):
    return {
        "record_id": f"CRM-{rid:04d}",
        "company_name": company,
        "contact_name": contact,
        "email": email,
        "phone": phone,
        "address": address,
        "city": city,
        "country": country,
        "website": website,
        "industry": industry or random.choice(INDUSTRIES),
        "account_owner": random.choice(SALES_REPS),
        "created_date": _rand_date((2022, 2024)),
        "last_activity": _rand_date((2024, 2025)),
        "revenue": _rand_revenue(),
        "status": random.choice(STATUSES),
    }


def generate_sample_data():
    """Generate 200 CRM records with intentional duplicate pairs."""
    records = []
    rid = 1

    # ============================================================
    # DEFINITE DUPLICATES (score 90+) — ~15 pairs
    # ============================================================

    # 1. Exact company, different contact
    loc = random.choice(CITIES_COUNTRIES)
    phone = _rand_phone(loc[0])
    records.append(_make_record(rid, "Daikin Industries Ltd", "Takeshi Yamamoto",
        "t.yamamoto@daikin.com", phone, "Gate City Ohsaki, 11-2 Osaki", "Tokyo", "Japan",
        "www.daikin.com", "HVAC")); rid += 1
    records.append(_make_record(rid, "Daikin Industries Ltd", "Kenji Sato",
        "k.sato@daikin.com", phone, "Gate City Ohsaki, 11-2 Osaki", "Tokyo", "Japan",
        "www.daikin.com", "HVAC")); rid += 1

    # 2. Typo in company name
    records.append(_make_record(rid, "Carrier Global Corporation", "John Smith",
        "j.smith@carrier.com", "+852 2891 0123", "Unit 2301, Tower 1, Lippo Centre", "Hong Kong", "Hong Kong",
        "www.carrier.com", "HVAC")); rid += 1
    records.append(_make_record(rid, "Carrier Global Corpration", "John Smith",
        "j.smith@carrier.com", "852-28910123", "Unit 2301, Tower 1 Lippo Centre", "Hong Kong", "Hong Kong",
        "www.carrier.com", "HVAC")); rid += 1

    # 3. Different formatting
    records.append(_make_record(rid, "Johnson Controls Int'l", "Peter Wang",
        "p.wang@johnsoncontrols.com", "+852 2528 9000", "15/F, One Pacific Place", "Hong Kong", "Hong Kong",
        "www.johnsoncontrols.com", "Building Services")); rid += 1
    records.append(_make_record(rid, "Johnson Controls International", "Peter Wang",
        "peter.wang@johnsoncontrols.com", "(852) 2528-9000", "15F One Pacific Place", "Hong Kong", "Hong Kong",
        "https://www.johnsoncontrols.com", "Building Services")); rid += 1

    # 4. Case inconsistency
    records.append(_make_record(rid, "DAIKIN INDUSTRIES", "Yuki Tanaka",
        "y.tanaka@daikin.com", "+81 6 6373 4312", "Umeda Center Bldg", "Tokyo", "Japan",
        "www.daikin.com", "HVAC")); rid += 1
    records.append(_make_record(rid, "daikin industries", "Yuki Tanaka",
        "y.tanaka@daikin.com", "81-66373-4312", "Umeda Center Building", "Tokyo", "Japan",
        "daikin.com", "HVAC")); rid += 1

    # 5. Slight name variation + same phone
    records.append(_make_record(rid, "Mitsubishi Electric Corporation", "Hiroshi Nakamura",
        "h.nakamura@mitsubishielectric.com", "+81 3 3218 2111", "Tokyo Building, 2-7-3 Marunouchi", "Tokyo", "Japan",
        "www.mitsubishielectric.com", "Manufacturing")); rid += 1
    records.append(_make_record(rid, "Mitsubishi Electric Corp.", "Hiroshi Nakamura",
        "h.nakamura@mitsubishielectric.com", "81-3-3218-2111", "Tokyo Bldg, 2-7-3 Marunouchi", "Tokyo", "Japan",
        "www.mitsubishielectric.com", "Manufacturing")); rid += 1

    # 6. Typo + address variation
    records.append(_make_record(rid, "Honeywell Building Technologies", "Sarah Johnson",
        "sarah.johnson@honeywell.com", "+852 2331 9133", "Suite 3001, ICC Tower", "Hong Kong", "Hong Kong",
        "www.honeywell.com", "Building Services")); rid += 1
    records.append(_make_record(rid, "Honeywell Buliding Technologies", "Sarah Johnson",
        "s.johnson@honeywell.com", "852-23319133", "Ste 3001 ICC Tower", "Hong Kong", "Hong Kong",
        "www.honeywell.com", "Building Services")); rid += 1

    # 7. Ltd vs Limited
    records.append(_make_record(rid, "Gree Electric Appliances Ltd", "Wei Zhang",
        "w.zhang@gree.com", "+86 756 8668 8888", "West Jinji Road, Qianshan", "Zhuhai", "China",
        "www.gree.com", "Manufacturing")); rid += 1
    records.append(_make_record(rid, "Gree Electric Appliances Limited", "Wei Zhang",
        "w.zhang@gree.com", "86-756-8668-8888", "West Jinji Road Qianshan", "Zhuhai", "China",
        "www.gree.com", "Manufacturing")); rid += 1

    # 8. Same company, different office format
    records.append(_make_record(rid, "Panasonic Corporation", "Akira Suzuki",
        "a.suzuki@panasonic.com", "+81 6 6908 1121", "1006 Kadoma, Kadoma-shi", "Osaka", "Japan",
        "www.panasonic.com", "Climate Technology")); rid += 1
    records.append(_make_record(rid, "Panasonic Corporation", "Takuya Ito",
        "t.ito@panasonic.com", "+81 6 6908 1121", "1006 Kadoma Kadoma City", "Osaka", "Japan",
        "panasonic.com", "Climate Technology")); rid += 1

    # 9. Corp vs Corporation
    records.append(_make_record(rid, "York International Corp", "Mike Chen",
        "m.chen@york.com", "+852 2590 0100", "22 Des Voeux Road", "Hong Kong", "Hong Kong",
        "www.york.com", "HVAC")); rid += 1
    records.append(_make_record(rid, "York International Corporation", "Mike Chen",
        "mike.chen@york.com", "(852) 2590-0100", "22 Des Voeux Rd Central", "Hong Kong", "Hong Kong",
        "www.york.com", "HVAC")); rid += 1

    # 10. Duplicate entry different date
    records.append(_make_record(rid, "Samsung HVAC Systems", "Jin Park",
        "j.park@samsung.com", "+82 2 2255 0114", "129 Samsung-ro, Yeongtong-gu", "Seoul", "South Korea",
        "www.samsung.com/hvac", "HVAC")); rid += 1
    records.append(_make_record(rid, "Samsung HVAC Systems", "Jin Park",
        "jin.park@samsung.com", "82-2-2255-0114", "129 Samsung-ro Yeongtong-gu", "Seoul", "South Korea",
        "www.samsung.com/hvac", "HVAC")); rid += 1

    # 11. Hitachi variations
    records.append(_make_record(rid, "Hitachi Air Conditioning", "Masa Kato",
        "m.kato@hitachi.com", "+81 3 3258 1111", "6-6 Marunouchi 1-chome", "Tokyo", "Japan",
        "www.hitachi.com", "HVAC")); rid += 1
    records.append(_make_record(rid, "Hitachi Air-Conditioning", "Masa Kato",
        "m.kato@hitachi.com", "81-33258-1111", "6-6 Marunouchi 1 Chome", "Tokyo", "Japan",
        "hitachi.com", "HVAC")); rid += 1

    # 12. Bosch formatting
    records.append(_make_record(rid, "Bosch Thermotechnology", "Hans Mueller",
        "h.mueller@bosch.com", "+49 6441 418 0", "Sophienstrasse 30-32", "Wetzlar", "Germany",
        "www.bosch-thermotechnology.com", "Climate Technology")); rid += 1
    records.append(_make_record(rid, "Bosch Thermo Technology", "Hans Mueller",
        "hans.mueller@bosch.com", "49-6441-418-0", "Sophienstr. 30-32", "Wetzlar", "Germany",
        "www.bosch-thermotechnology.com", "Climate Technology")); rid += 1

    # 13. Lennox typo
    records.append(_make_record(rid, "Lennox International Inc", "Tom Davis",
        "t.davis@lennox.com", "+1 972 497 5000", "2140 Lake Park Blvd", "Richardson", "USA",
        "www.lennox.com", "HVAC")); rid += 1
    records.append(_make_record(rid, "Lennox Interntional Inc.", "Tom Davis",
        "t.davis@lennox.com", "1-972-497-5000", "2140 Lake Park Boulevard", "Richardson", "USA",
        "lennox.com", "HVAC")); rid += 1

    # 14. Rheem duplicate
    records.append(_make_record(rid, "Rheem Manufacturing Company", "Steve Brown",
        "s.brown@rheem.com", "+1 405 260 3500", "1100 Abernathy Road NE", "Atlanta", "USA",
        "www.rheem.com", "Manufacturing")); rid += 1
    records.append(_make_record(rid, "Rheem Manufacturing Co.", "Steve Brown",
        "steve.brown@rheem.com", "(1) 405-260-3500", "1100 Abernathy Rd NE", "Atlanta", "USA",
        "www.rheem.com", "Manufacturing")); rid += 1

    # 15. Fujitsu General
    records.append(_make_record(rid, "Fujitsu General Limited", "Yoko Sato",
        "y.sato@fujitsu-general.com", "+81 44 866 1111", "3-3-17 Suenaga, Takatsu-ku", "Kawasaki", "Japan",
        "www.fujitsu-general.com", "HVAC")); rid += 1
    records.append(_make_record(rid, "Fujitsu General Ltd", "Yoko Sato",
        "y.sato@fujitsu-general.com", "81-44-866-1111", "3-3-17 Suenaga Takatsu", "Kawasaki", "Japan",
        "fujitsu-general.com", "HVAC")); rid += 1

    # ============================================================
    # PROBABLE DUPLICATES (score 75-89) — ~10 pairs
    # ============================================================

    # 1. Abbreviation
    records.append(_make_record(rid, "Trane Technologies PLC", "Amy Wilson",
        "a.wilson@trane.com", "+1 704 655 4000", "800-E Beaty Street", "Davidson", "USA",
        "www.tranetechnologies.com", "HVAC")); rid += 1
    records.append(_make_record(rid, "Trane Tech", "Amy Wilson",
        "amy.w@trane.com", "+1 704 655 4000", "800E Beaty St", "Davidson", "USA",
        "www.trane.com", "HVAC")); rid += 1

    # 2. Regional variant
    records.append(_make_record(rid, "Mitsubishi Electric Asia", "Kevin Lim",
        "k.lim@mitsubishielectric.sg", "+65 6473 2308", "307 Alexandra Road", "Singapore", "Singapore",
        "www.mitsubishielectric.com.sg", "Manufacturing")); rid += 1
    records.append(_make_record(rid, "Mitsubishi Electric (HK)", "Kevin Lam",
        "k.lam@mitsubishielectric.hk", "+852 2510 0555", "8 Finance Street", "Hong Kong", "Hong Kong",
        "www.mitsubishielectric.hk", "Manufacturing")); rid += 1

    # 3. Different office same company
    records.append(_make_record(rid, "Honeywell Building Solutions", "Rachel Lee",
        "r.lee@honeywell.com", "+852 2331 9133", "Suite 2001, ICC Tower", "Hong Kong", "Hong Kong",
        "www.honeywell.com", "Building Services")); rid += 1
    records.append(_make_record(rid, "Honeywell Hong Kong Ltd", "Rachel Lee",
        "rachel.lee@honeywell.com", "+852 2331 9200", "23/F, Tower 6, The Gateway", "Hong Kong", "Hong Kong",
        "www.honeywell.com/hk", "Building Services")); rid += 1

    # 4. Merged / acquired
    records.append(_make_record(rid, "Emerson Climate Technologies", "David Chan",
        "d.chan@emerson.com", "+852 2736 6339", "Unit 1901, Miramar Tower", "Hong Kong", "Hong Kong",
        "www.emersonclimate.com", "Climate Technology")); rid += 1
    records.append(_make_record(rid, "Copeland (formerly Emerson)", "David Chan",
        "d.chan@copeland.com", "+852 2736 6339", "Unit 1901, Miramar Tower, Tsim Sha Tsui", "Hong Kong", "Hong Kong",
        "www.copeland.com", "Climate Technology")); rid += 1

    # 5. Haier regional
    records.append(_make_record(rid, "Haier Group Corporation", "Lisa Wang",
        "l.wang@haier.com", "+86 532 8893 9999", "Haier Road, Hi-tech Zone", "Qingdao", "China",
        "www.haier.com", "Manufacturing")); rid += 1
    records.append(_make_record(rid, "Haier Smart Home Co", "Lisa Wang",
        "lisa.wang@haier.com", "+86 532 8893 8888", "1 Haier Road", "Qingdao", "China",
        "www.haier.net", "Manufacturing")); rid += 1

    # 6. Midea variations
    records.append(_make_record(rid, "Midea Group Co Ltd", "Frank Li",
        "f.li@midea.com", "+86 757 2660 4888", "6 Midea Avenue, Beijiao", "Foshan", "China",
        "www.midea.com", "Manufacturing")); rid += 1
    records.append(_make_record(rid, "Midea HVAC Equipment", "Frank Li",
        "frank.li@midea.com", "+86 757 2660 4888", "Midea Avenue Beijiao Town", "Foshan", "China",
        "www.midea.com/hvac", "HVAC")); rid += 1

    # 7. Swire Properties
    records.append(_make_record(rid, "Swire Properties Limited", "Alan Chow",
        "a.chow@swireproperties.com", "+852 2844 3888", "33/F, One Island East", "Hong Kong", "Hong Kong",
        "www.swireproperties.com", "Property Management")); rid += 1
    records.append(_make_record(rid, "Swire Properties HK", "Alan Chow",
        "alan.chow@swireproperties.com", "+852 2844 3800", "One Island East Taikoo Place", "Hong Kong", "Hong Kong",
        "www.swireproperties.com", "Property Management")); rid += 1

    # 8. Dragon Air Engineering
    records.append(_make_record(rid, "Dragon Air Engineering HK", "Tony Wu",
        "t.wu@dragonair-eng.com", "+852 2345 6789", "Unit 501, Cyberport 3", "Hong Kong", "Hong Kong",
        "www.dragonair-eng.com", "Engineering")); rid += 1
    records.append(_make_record(rid, "Dragon Air Engineering Limited", "Tony Wu",
        "tony.wu@dragonair-eng.com", "+852 2345 6790", "501 Cyberport Three", "Hong Kong", "Hong Kong",
        "www.dragonair-eng.com.hk", "Engineering")); rid += 1

    # 9. Pacific HVAC
    records.append(_make_record(rid, "Pacific HVAC Solutions Pte Ltd", "Ben Tan",
        "b.tan@pacifichvac.com", "+65 6789 0123", "50 Raffles Place", "Singapore", "Singapore",
        "www.pacifichvac.com", "HVAC")); rid += 1
    records.append(_make_record(rid, "Pacific HVAC Solutions", "Benjamin Tan",
        "ben.tan@pacifichvac.com", "+65 6789 0123", "50 Raffles Place #30-01", "Singapore", "Singapore",
        "www.pacifichvac.com.sg", "HVAC")); rid += 1

    # 10. Sun Hung Kai
    records.append(_make_record(rid, "Sun Hung Kai Properties", "Chris Fung",
        "c.fung@shkp.com", "+852 2827 8111", "45/F, Sun Hung Kai Centre", "Hong Kong", "Hong Kong",
        "www.shkp.com", "Property Management")); rid += 1
    records.append(_make_record(rid, "Sun Hung Kai Properties Ltd", "Christopher Fung",
        "chris.fung@shkp.com", "+852 2827 8112", "Sun Hung Kai Centre, 30 Harbour Rd", "Hong Kong", "Hong Kong",
        "www.shkp.com.hk", "Property Management")); rid += 1

    # ============================================================
    # POSSIBLE DUPLICATES (score 60-74) — ~8 pairs
    # ============================================================

    # 1. Similar names, different entities
    records.append(_make_record(rid, "Asia Air Conditioning Co", "William Lau",
        "w.lau@asiaac.com", "+852 2555 1234", "100 Nathan Road", "Hong Kong", "Hong Kong",
        "www.asiaac.com", "HVAC")); rid += 1
    records.append(_make_record(rid, "Asia AC Solutions Ltd", "William Lau",
        "w.lau@asiaac-solutions.com", "+852 2555 4321", "88 Nathan Road", "Hong Kong", "Hong Kong",
        "www.asiaac-solutions.com", "HVAC")); rid += 1

    # 2. Parent / subsidiary
    records.append(_make_record(rid, "Danfoss Group", "Erik Jensen",
        "e.jensen@danfoss.com", "+45 7488 2222", "Nordborgvej 81", "Nordborg", "Denmark",
        "www.danfoss.com", "Climate Technology")); rid += 1
    records.append(_make_record(rid, "Danfoss Hong Kong", "Mary Cheung",
        "m.cheung@danfoss.com.hk", "+852 2590 8700", "12 Marina Boulevard", "Hong Kong", "Hong Kong",
        "www.danfoss.com/hk", "Climate Technology")); rid += 1

    # 3. Different brand entity
    records.append(_make_record(rid, "LG Electronics HVAC", "Sung Kim",
        "s.kim@lge.com", "+82 2 3777 1114", "128 Yeoui-daero", "Seoul", "South Korea",
        "www.lg.com/hvac", "HVAC")); rid += 1
    records.append(_make_record(rid, "LG Air Solution", "Min Kim",
        "m.kim@lgairsolution.com", "+82 2 3777 2000", "LG Twin Towers", "Seoul", "South Korea",
        "www.lgairsolution.com", "HVAC")); rid += 1

    # 4. Greater Bay Area variations
    records.append(_make_record(rid, "Greater Bay Area Cooling Systems", "Jack Ma",
        "j.ma@gbacooling.com", "+86 755 8832 0000", "Nanshan District", "Shenzhen", "China",
        "www.gbacooling.com", "HVAC")); rid += 1
    records.append(_make_record(rid, "GBA Cooling Systems Ltd", "Jack Ma",
        "jack.ma@gbacooling.hk", "+852 3102 5566", "Block A, Science Park", "Hong Kong", "Hong Kong",
        "www.gbacooling.com.hk", "HVAC")); rid += 1

    # 5. Cathay Pacific Services
    records.append(_make_record(rid, "Cathay Pacific Services Ltd", "Annie Ng",
        "a.ng@cathaypacific.com", "+852 2747 5000", "Cathay City, HK Airport", "Hong Kong", "Hong Kong",
        "www.cathaypacific.com", "Facilities Management")); rid += 1
    records.append(_make_record(rid, "Cathay Pacific Catering Services", "Annie Ng",
        "a.ng@cpcs.com.hk", "+852 2747 5100", "Catering Road, HK Airport", "Hong Kong", "Hong Kong",
        "www.cpcs.com.hk", "Facilities Management")); rid += 1

    # 6. MTR Corporation
    records.append(_make_record(rid, "MTR Corporation", "Gary Lam",
        "g.lam@mtr.com.hk", "+852 2993 2111", "MTR Headquarters Building", "Hong Kong", "Hong Kong",
        "www.mtr.com.hk", "Property Management")); rid += 1
    records.append(_make_record(rid, "MTR Corp Engineering", "Gary Lam",
        "gary.lam@mtr.com.hk", "+852 2993 2200", "Telford Plaza, Kowloon Bay", "Hong Kong", "Hong Kong",
        "www.mtr.com.hk/engineering", "Engineering")); rid += 1

    # 7. Hospital Authority
    records.append(_make_record(rid, "Hospital Authority HK", "Dr. Susan Cheng",
        "s.cheng@ha.org.hk", "+852 2300 6555", "147B Argyle Street", "Hong Kong", "Hong Kong",
        "www.ha.org.hk", "Facilities Management")); rid += 1
    records.append(_make_record(rid, "Hospital Authority", "Dr. Susan Cheng",
        "susan.cheng@ha.org.hk", "+852 2300 6000", "Hospital Authority Building, Argyle St", "Hong Kong", "Hong Kong",
        "www.ha.org.hk", "Facilities Management")); rid += 1

    # 8. HK International Airport
    records.append(_make_record(rid, "HK International Airport", "Raymond Yip",
        "r.yip@hkairport.com", "+852 2188 7111", "1 Sky Plaza Road, Chek Lap Kok", "Hong Kong", "Hong Kong",
        "www.hongkongairport.com", "Facilities Management")); rid += 1
    records.append(_make_record(rid, "Hong Kong Intl Airport Authority", "Raymond Yip",
        "raymond.yip@aa.gov.hk", "+852 2188 7000", "HKIA Tower", "Hong Kong", "Hong Kong",
        "www.hongkongairport.com", "Facilities Management")); rid += 1

    # ============================================================
    # CLEAN RECORDS — fill to 200 total
    # ============================================================
    clean_companies = [
        ("Schneider Electric SE", "schneider-electric.com", "Energy Solutions"),
        ("Siemens Building Technologies", "siemens.com", "Building Services"),
        ("ABB Ltd", "abb.com", "Manufacturing"),
        ("Emerson Electric Co", "emerson.com", "Manufacturing"),
        ("Danfoss Climate Solutions SG", "danfoss-sg.com", "Climate Technology"),
        ("Grundfos Pumps Pte Ltd", "grundfos.com", "Manufacturing"),
        ("Belimo Actuators Ltd", "belimo.com", "Building Services"),
        ("Systemair AB", "systemair.com", "HVAC"),
        ("Nortek Global HVAC", "nortekhvac.com", "HVAC"),
        ("Bard Manufacturing", "bardhvac.com", "Manufacturing"),
        ("Heatcraft Worldwide Refrigeration", "heatcraftrpd.com", "Refrigeration"),
        ("Hussmann Corporation", "hussmann.com", "Refrigeration"),
        ("Manitowoc Ice", "manitowocice.com", "Refrigeration"),
        ("Welbilt Inc", "welbilt.com", "Manufacturing"),
        ("SPX Cooling Technologies", "spxcooling.com", "Climate Technology"),
        ("Alfa Laval AB", "alfalaval.com", "Manufacturing"),
        ("GEA Group AG", "gea.com", "Manufacturing"),
        ("Bitzer SE", "bitzer.de", "Refrigeration"),
        ("Embraco (Nidec)", "embraco.com", "Manufacturing"),
        ("Secop GmbH", "secop.com", "Manufacturing"),
        ("Tecumseh Products", "tecumseh.com", "Manufacturing"),
        ("Rivacold SRL", "rivacold.com", "Refrigeration"),
        ("Lu-Ve SpA", "luve.it", "HVAC"),
        ("Airedale International", "airedale.com", "HVAC"),
        ("Climaveneta SpA", "climaveneta.com", "HVAC"),
        ("Stulz GmbH", "stulz.com", "Climate Technology"),
        ("Vertiv Holdings", "vertiv.com", "Climate Technology"),
        ("Munters Group AB", "munters.com", "Climate Technology"),
        ("Condair Group AG", "condair.com", "Climate Technology"),
        ("Dantherm Group", "dantherm.com", "Climate Technology"),
        ("Asia Cold Chain Logistics", "asiacoldchain.com", "Refrigeration"),
        ("Jardine Engineering Corporation", "jec.com", "Engineering"),
        ("Gammon Construction Limited", "gammon.com.hk", "Construction"),
        ("Hip Hing Construction Co", "hiphing.com.hk", "Construction"),
        ("China State Construction Intl", "csci.com.hk", "Construction"),
        ("Henderson Land Development", "hld.com", "Property Management"),
        ("New World Development", "nwd.com.hk", "Property Management"),
        ("Cheung Kong Holdings", "ckh.com.hk", "Property Management"),
        ("Hang Lung Properties", "hanglungproperties.com", "Property Management"),
        ("Kerry Properties Limited", "kerryprops.com", "Property Management"),
        ("Hysan Development Company", "hysan.com.hk", "Property Management"),
        ("Link REIT", "linkreit.com", "Property Management"),
        ("Sino Land Company", "sino.com", "Property Management"),
        ("Wharf Holdings Limited", "wharfholdings.com", "Property Management"),
        ("CLP Holdings Limited", "clpgroup.com", "Energy Solutions"),
        ("HK Electric Investments", "hkelectric.com", "Energy Solutions"),
        ("Towngas (HK & China Gas)", "towngas.com", "Energy Solutions"),
        ("AIA Group Limited", "aia.com", "Facilities Management"),
        ("HSBC Holdings plc", "hsbc.com", "Facilities Management"),
        ("Standard Chartered HK", "sc.com", "Facilities Management"),
        ("Hang Seng Bank", "hangseng.com", "Facilities Management"),
        ("Bank of China (HK)", "bochk.com", "Facilities Management"),
        ("Mapletree Industrial Trust", "mapletree.com.sg", "Property Management"),
        ("CapitaLand Investment", "capitaland.com", "Property Management"),
        ("City Developments Limited", "cdl.com.sg", "Property Management"),
        ("Keppel Corporation", "kepcorp.com", "Engineering"),
        ("Sembcorp Industries", "sembcorp.com", "Energy Solutions"),
        ("Thai Union Group PCL", "thaiunion.com", "Manufacturing"),
        ("PTT Global Chemical", "pttgcgroup.com", "Energy Solutions"),
        ("Charoen Pokphand Group", "cpgroupglobal.com", "Manufacturing"),
        ("San Miguel Corporation", "sanmiguel.com.ph", "Manufacturing"),
        ("Ayala Corporation", "ayala.com.ph", "Property Management"),
        ("SM Investments Corporation", "sminvestments.com", "Property Management"),
        ("Vingroup JSC", "vingroup.net", "Property Management"),
        ("Siam Cement Group", "scg.com", "Construction"),
        ("Aboitiz Power Corp", "aboitizpower.com", "Energy Solutions"),
        ("First Gen Corporation", "firstgen.com.ph", "Energy Solutions"),
        ("Reliance Industries Ltd", "ril.com", "Manufacturing"),
        ("Tata Projects Limited", "tataprojects.com", "Construction"),
        ("Larsen & Toubro Ltd", "larsentoubro.com", "Construction"),
        ("Godrej & Boyce Mfg", "godrej.com", "Manufacturing"),
        ("Blue Star Limited", "bluestarindia.com", "HVAC"),
        ("Voltas Limited", "voltas.com", "HVAC"),
        ("Emaar Properties PJSC", "emaar.com", "Property Management"),
        ("Aldar Properties PJSC", "aldar.com", "Property Management"),
        ("Saudi Electricity Company", "se.com.sa", "Energy Solutions"),
        ("ACWA Power", "acwapower.com", "Energy Solutions"),
        ("Zamil Industrial Investment", "zamil.com", "Manufacturing"),
        ("Al Salem Johnson Controls", "alsalemjci.com", "HVAC"),
        ("National Refrigeration Co", "natref.com", "Refrigeration"),
        ("Emirates Central Cooling", "empower.ae", "Climate Technology"),
        ("Tabreed (National Central Cooling)", "tabreed.ae", "Climate Technology"),
        ("Drake & Scull International", "drakescull.com", "Engineering"),
        ("Remind GmbH", "remind.de", "Climate Technology"),
        ("Arctic King Appliances", "arcticking.com", "HVAC"),
        ("Cooltech Applications SA", "cooltech-applications.com", "Climate Technology"),
        ("Hisense Home Appliances", "hisense.com", "Manufacturing"),
        ("TCL Air Conditioner", "tcl.com", "HVAC"),
        ("Aux Group Co Ltd", "aux.cn", "HVAC"),
        ("Chigo Air Conditioning", "chigo.com", "HVAC"),
        ("Tica Thermal Technology", "tica.com.cn", "Climate Technology"),
        ("Eurovent Certita Certification", "eurovent-certification.com", "HVAC"),
        ("Rosenberg Ventilatoren GmbH", "rosenberg-gmbh.com", "HVAC"),
        ("Ziehl-Abegg SE", "ziehl-abegg.com", "Manufacturing"),
        ("ebm-papst Group", "ebmpapst.com", "Manufacturing"),
        ("Nibe Industrier AB", "nibe.com", "Climate Technology"),
        ("Viessmann Climate Solutions", "viessmann.com", "Climate Technology"),
        ("Vaillant Group", "vaillant-group.com", "Climate Technology"),
        ("Stiebel Eltron GmbH", "stiebel-eltron.com", "Climate Technology"),
        ("Wolf GmbH", "wolf.eu", "HVAC"),
        ("Kronoterm Heat Pumps", "kronoterm.com", "Climate Technology"),
        ("NZXT Cooling Solutions", "nzxt-cooling.com", "Climate Technology"),
        ("Glen Dimplex Group", "glendimplex.com", "Climate Technology"),
        ("De Longhi SpA", "delonghi.com", "Manufacturing"),
        ("Mitsubishi Heavy Industries", "mhi.com", "Manufacturing"),
        ("IHI Corporation", "ihi.co.jp", "Manufacturing"),
        ("Kawasaki Heavy Industries", "khi.co.jp", "Manufacturing"),
        ("Daikin Applied Americas", "daikinapplied.com", "HVAC"),
        ("Toshiba Carrier Corporation", "toshiba-carrier.co.jp", "HVAC"),
        ("Carel Industries SpA", "carel.com", "Climate Technology"),
        ("Watlow Electric Manufacturing", "watlow.com", "Manufacturing"),
        ("Ingersoll Rand Inc", "ingersollrand.com", "Manufacturing"),
        ("Wilo SE", "wilo.com", "Manufacturing"),
        ("Xylem Inc", "xylem.com", "Manufacturing"),
        ("Rinnai Corporation", "rinnai.co.jp", "HVAC"),
        ("Noritz Corporation", "noritz.co.jp", "HVAC"),
        ("A.O. Smith Corporation", "aosmith.com", "Manufacturing"),
        ("Therma-Wave Industries", "thermawave.com", "Climate Technology"),
        ("Ice Energy Holdings", "ice-energy.com", "Energy Solutions"),
        ("Coolsys Inc", "coolsys.com", "Refrigeration"),
        ("RefrigiWear Inc", "refrigiwear.com", "Refrigeration"),
        ("Uniflair SpA", "uniflair.com", "Climate Technology"),
        ("Kaltra Innovativtechnik", "kaltra.com", "HVAC"),
        ("Swegon Group AB", "swegon.com", "HVAC"),
        ("FläktGroup", "flaktgroup.com", "HVAC"),
        ("Trox GmbH", "trox.de", "HVAC"),
        ("Systemair Group", "systemairgroup.com", "HVAC"),
        ("Taikisha Ltd", "taikisha.co.jp", "Engineering"),
        ("Kirby Building Systems", "kirbyinternational.com", "Construction"),
        ("Al Habtoor Group", "habtoor.com", "Construction"),
        ("Samsung C&T Corporation", "samsungcnt.com", "Construction"),
        ("Hyundai Engineering", "hdec.kr", "Construction"),
        ("Posco International", "poscointl.com", "Manufacturing"),
        ("Doosan Enerbility", "doosanenerbility.com", "Energy Solutions"),
    ]

    first_names = ["James", "Emma", "Liam", "Olivia", "Noah", "Ava", "William", "Sophia",
                   "Oliver", "Isabella", "Benjamin", "Mia", "Lucas", "Charlotte", "Henry",
                   "Amelia", "Alexander", "Harper", "Daniel", "Evelyn", "Michael", "Grace",
                   "Andrew", "Victoria", "Thomas", "Lily", "Nathan", "Ella", "Kevin", "Chloe"]
    last_names = ["Wong", "Chen", "Lee", "Kim", "Tanaka", "Singh", "Patel", "Nguyen",
                  "Santos", "Garcia", "Mueller", "Schmidt", "Andersen", "Johansson", "Rossi",
                  "Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Wilson", "Taylor",
                  "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson"]

    for company, domain, industry in clean_companies:
        city, country = random.choice(CITIES_COUNTRIES)
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        email_prefix = f"{fname[0].lower()}.{lname.lower()}"
        use_company_email = random.random() > 0.1
        email_domain = domain if use_company_email else random.choice(["gmail.com", "yahoo.com", "outlook.com"])
        email = f"{email_prefix}@{email_domain}"

        phone = _rand_phone(city) if random.random() > 0.10 else ""
        if random.random() < 0.05:
            email = ""

        records.append(_make_record(
            rid, company, f"{fname} {lname}", email, phone,
            random.choice(STREETS), city, country,
            f"www.{domain}", industry
        ))
        rid += 1
        if len(records) >= 200:
            break

    # Ensure exactly 200 records
    records = records[:200]
    return pd.DataFrame(records)


def save_sample_data(output_path="data/sample_crm.csv"):
    """Generate and save sample data to CSV."""
    df = generate_sample_data()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} records -> {output_path}")
    return df


if __name__ == "__main__":
    df = save_sample_data()
    print(f"\nColumns: {list(df.columns)}")
    print(f"Sample:\n{df.head()}")
