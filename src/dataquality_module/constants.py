""" Common words and phrases provided by the PEP team
"""

COMMON_ENGLISH_WORDS = [
    "the",
    "of",
    "and",
    "to",
    "in",
    "for",
    "is",
    "on",
    "that",
    "by",
    "this",
    "with",
    "you",
    "it",
    "not",
    "or",
    "be",
    "are",
    "from",
    "at",
    "as",
    "your",
    "all",
    "have",
    "new",
    "an",
    "was",
    "we",
    "home",
    "us",
    "about",
    "if",
    "has",
    "search",
    "free",
    "but",
    "our",
    "one",
    "other",
    "information",
    "time",
    "they",
    "site",
    "up",
    "what",
    "which",
    "their",
    "news",
    "out",
    "use",
    "any",
    "there",
    "only",
    "so",
    "his",
    "when",
    "contact",
    "here",
    "business",
    "who",
    "web",
    "also",
    "now",
    "help",
    "get",
    "pm",
    "view",
    "online",
    "first",
    "am",
    "been",
    "would",
    "how",
    "were",
    "me",
    "services",
    "some",
    "these",
    "click",
    "its",
    "like",
    "service",
    "than",
    "find",
    "date",
    "back",
    "top",
    "people",
    "had",
    "list",
    "name",
    "just",
    "over",
    "state",
    "year",
    "into",
    "email",
    "two",
    "health",
    "world",
    "re",
    "next",
    "used",
    "go",
    "work",
    "last",
    "most",
    "products",
    "music",
    "buy",
    "data",
    "make",
    "them",
    "should",
    "product",
    "system",
    "post",
    "her",
    "city",
    "add",
    "policy",
    "number",
    "such",
    "please",
    "available",
    "copyright",
    "support",
    "message",
    "after",
    "best",
    "software",
    "then",
    "jan",
    "good",
    "video",
    "well",
    "where",
    "info",
    "rights",
    "public",
    "books",
    "high",
    "school",
    "through",
    "each",
    "links",
    "she",
    "review",
    "years",
    "order",
    "very",
    "privacy",
    "book",
    "items",
    "company",
    "read",
    "group",
    "sex",
    "need",
    "many",
    "user",
    "said",
    "de",
    "does",
    "set",
    "under",
    "general",
    "research",
    "university",
    "january",
    "mail",
    "full",
    "map",
    "reviews",
    "program",
    "life",
    "know",
    "games",
    "way",
    "days",
    "management",
    "part",
    "could",
    "great",
    "united",
    "hotel",
    "real",
    "item",
    "international",
    "center",
    "ebay",
    "must",
    "store",
    "travel",
    "comments",
    "made",
    "development",
    "report",
    "off",
]


DEFAULT_HONORIFICS = [
    "mr",
    "mister",
    "ms",
    "miss",
    "mrs",
    "dr",
    "doctor",
    "phd",
    "prof",
    "professor",
    "eng",
    "sir",
    "doc",
    "judge",
    "adv",
    "advocate",
    "king",
    "queen",
    "lord",
    "lady",
    "prince",
    "princess",
    "earl",
    "baroness",
    "baron",
    "duke",
    "duchess",
    "marquess",
    "marchioness",
    "viscount",
    "viscountess",
    "honourable",
]

INDONESIA_HONORIFICS = [
    "hj",
    "h",
    "ir",
    "i.b",
    "ida bagus",
    "i.a",
    "ida ayu",
    "a.a",
    "anak agung",
    "cok",
    "cokorda",
    "gst",
    "gusti",
    "dw",
    "dewa",
    "ngkn",
    "ngakan",
    "dsk",
    "desak",
    "drs",
    "se",
    "mm",
    "m.si",
    "sh",
    "s.ag.",
    "kh",
    "se",
    "h.",
    "dra. ir.",
    "m.kes.",
    "pdt.",
    "s.sos.",
    "s.h.",
    "m.sp",
]

ISRAEL_HONORIFICS = ['ד"ר', "adv.", 'עו"ד', "פרופסור", "גב'"]

MALAYSIA_HONORIFICS = [
    "datuk",
    "dato sri",
    "dato seri",
    "datuk seri",
    "dato",
    "datins",
    "tun",
    "tan seri",
    "tan sri",
    "encik",
    "en",
    "tuan",
    "rn",
    "tuan yang terutama",
    "puan",
    "madame",
    "cik",
    "tpr",
    "registered town planner",
    "tuan yang terutama",
    "tyt",
    "yang amat berhormat",
    "yab",
    "yang berhormat",
    "yb",
    "yang berhormat mulia",
    "ybm",
    "yang amat arif",
    "yaa",
    "yang arif",
    "ya",
    "yang amat berbahagia",
    "yabhg",
    "yang berbahagia",
    "ybhg",
    "Dato' Indera",
    "Puan Sri",
    "Seri",
    "datin",
    "Y.A.M.",
    "Tengku",
    "YBhg.",
    "YM RAJA",
    "YBM.",
    "YH.",
    "Y.Bhg.",
    "Prof Madya",
    "Emeritus",
    "Setia",
    "Pengiran",
    "Dayang",
    "Paduka",
    "Awang",
    "Yang Berhormat"
]

NIGERIA_HONORIFICS = ["alhaji", "alh", "barrister", "barr", "barr."," FNSE", " SAN", " MNI", " MFR"] 
                                    # not sure if we can keep (FNSE", " SAN", " MNI", " MFR)

SOUTH_AFRICA_HONORICIS = ["inkosi"]

THAILAND_HONORIFICS = [
    # general honorifics
    "นาย",  # mr
    "นาง",  # mrs
    "หม่ sau ม.ล.",  # ML
    "นายแพทย์",  # doctor
    "นพ. sau พญ.",  # dr./M.D.
    "ศรี",  # Sri
    "คุณ",  # Sir/Mister
    "นางสาว",  # Ms.
    "ม.ร.ว.",  # M.R.
    "นา",  # Miss
    "ดร.",  # Dr.
    "รศ.ดร.มั sau ศ.ดร.นพ. sau รศ.ดร.",  # Prof. Dr.(sau Assoc. Prof. Dr.)
    "ศาตราจารย์ sau ศาสตราจ",  # professor
    "นางสา",  # Mrs.
    "ผศ.นพ.",  # Assistant Professor
    "รองศาสตราจารย์ ดร.",  # Associate Professor Dr.
    "ผู้ช่วยศาสตราจารย์ ดร.",  # Assistant Professor Dr.
    "ศาสตราจารย์เกียรติคุณ",  # Professor Emeritus
    "ศาสตราจารย์พิเศษ",  # Special Professor
    "ทันตแพทย์",  # dentist
    "น.ส.",  # Miss
    # ranks
    "พลเอก",
    "พล.ท.",  #  General
    "พลอากาศเอก",
    "พลอากาศตรี",  #  Air Chief Marshal
    "พลเรือเอก",
    "พลเรือตรี",  #  Admiral
    "ร้อยโท",
    "พลโท",
    "ว่าที่ร้อยตรี",  #  Lieutenant, Acting Lieutenant
    "ร้อยตรี",  #  Second Lieutenant
    "พันโท",
    "พันตำรวจตรี",  #  Lieutenant Colonel
    "พลตำรวจโท",  #  Lieutenant General
    "พันตำรวจโท",  #  Police lieutenant colonel
    "พ.ต.อ.",  #  Pol. colonel
    "พลตำรวจเอก",  #  Police General
    "พลตำรวจตรี",  #  Police Major General
    "พันจ่าตรี",  #  Major Sergeant(or Chief Petty Officer)
    "พลตรี",
    "พล.ต.ต.",  #  Major General
    "ร้อยตำรวจโทหญิง",  #  Female Police Lieutenant
    "ร้อยเอก",  #  Captain
    "พันจ่าเอก",  #  Colonel/Major Sergeant
    "พันเอก",
    "พันตำรวจเอก",  #  Colonel
    "ว่าที่ร.ต.หญิง",  #  Acting Lieutenant Female(or Acting Sub Lieutenant, translation is pretty bad)
    # police ranks
    "พล.ต.อ.",
    "พลตำรวจเอก",  # POLICE  GENERAL  ( POL . GEN . )
    "พล.ต.ท.",
    "พลตำรวจโท",  # POLICE  LIEUTENANT  GENERAL  ( POL . LT . GEN . )
    "พล.ต.ต.",
    "พลตำรวจตรี",  # POLICE  MAJOR  GENERAL  ( POL . MAJ . GEN . )
    "พ.ต.อ.",
    "พันตำรวจเอก",  # POLICE  COLONEL  ( POL . COL . )
    "พ.ต.ท.",
    "พันตำรวจโท",  # POLICE  LIEUTENANT  COLONEL  ( POL . LT . COL . )
    "พ.ต.ต.",
    "พันตำรวจตรี",  # POLICE  MAJOR  ( POL . MAJ . )
    "ร.ต.อ.",
    "ร้อยตำรวจเอก",  # POLICE  CAPTAIN  ( POL . CAPT . )
    "ร.ต.ท.",
    "ร้อยตำรวจโท",  # POLICE  LIEUTENANT  ( POL . LT . )
    "ร.ต.ต.",
    "ร้อยตำรวจตรี",  # POLICE  SUB - LIEUTENANT  ( POL . SUB . LT . )
    "ด.ต.",
    "ดาบตำรวจ",  # POLICE  SENIOR  SERGEANT  MAJOR  ( POL . SEN . SGT . MAJ . )
    "จ.ส.ต.",
    "จ่าสิบตำรวจ",  # POLICE  SERGEANT  MAJOR  ( POL . SGT . MAJ . )
    "ส.ต.อ.",
    "สิบตำรวจเอก",  # POLICE  SERGEANT  ( POL . SGT . )
    "ส.ต.ท.",
    "สิบตำรวจโท",  # POLICE  CORPORAL  ( POL . CPL . )
    "ส.ต.ต.",
    "สิบตำรวจตรี",  # POLICE  LANCE  CORPORAL  ( POL . L / C . )
    # common titles
    "ผู้บังคับหมู่",  # SERVICEMAN
    "รองสารวัตร",  # SQUAD  LEADER
    "สารวัุตร",  # INSPECTOR
    "สารวัตรอำนวยการ",  # STAFF  INSPECTOR
    "สารวัตรสืบสวนสอบสวน",  # INVESTIGATION  INSPECTOR
    "สารวัตรปกครองป้องกัน",  # ADMINISTRATION  INSPECTOR
    "สารวัตรจราจร",  # TRAFFIC  INSPECTOR
    "รองผู้กำกับการ",  # DEPUTY  SUPERINTENDENT
    "ผู้กำกับการ",  # SUPERINTENDENT
    "รองผู้บังคับการ",  # DEPUTY  COMMANDER
    "ผู้บังคับการ",  # COMMANDER
    "จเรตำรวจ",  # INSPECTOR - GENERAL
    "รองผู้บัญชาการ",  # DEPUTY  COMMISSIONER
    "ผู้บัญชาการ",  # COMMISSIONER
    "ผู้ช่วยผู้บัญชาการตำรวจแห่งชาติ",  # ASSISTANT DIRECTOR-GENERAL OF THE ROYAL THAI POLICE  DEPARTMEMT
    "รองผู้บัญชาการตำรวจแห่งชาติ",  # DEPUTY DIRECTOR-GENERAL OF THE ROYAL THAI POLICE DEPARTMEMT
    "ผู้บัญชาการตำรวจแห่งชาติ",  # DIRECTOR-GENERAL OF THE ROYAL THAI POLICE DEPARTMEMT
    # royal descendants
    "หม่อมหลวง",  # Mom Luang
    "ณ อยุธยา",  # Na Ayutthaya
]

VIETNAM_HONORIFICS = [
    "Đồng chí",  # Comrades
    "Giáo sư",
    "Viện sĩ",  # Professor, Academy
    "Giáo sư",  # Professor
    "GS.TS.",  # Professor Dr.
    "Phó Giáo sư",
    "Tiến sĩ",  # Associate Professor Ph.D
    "PGS.TS.",  #  Associate Professor Ph.D
    "TS.",  # Dr / Ph.D
    "TS.NCVC.",
    "Ths",  # Master
    "ThS. Bs",  # Master doctor
    "Ths.CVC.",  # Master
    "ÔNG",  # Mr.
    "BÀ",  # Ms.
    "Đ",
    "c",  # Mr / Ms
    "Đại tướng",  # General
    "Đại tá",  # Colonel
    "Linh mục",  # Priests
    "Thượng tướng",  # Upper Minister
    "Hòa thượng",  # Venerable
    "Giáo hữu",  # believers
]

UNITED_KINGDOM_HONORIFICS = [
    "GBE",
    "KBE",
    "DBE",
    "CBE",
    "OBE",
    "MBE",
    "BEM",
    "RVO",
    "MEP",
    "ministers of religion",
    "KC",
    "MP",
    "QC",
    "Rev",    
]

MACEDONIA_HONORIFICS = [
    "Г-дин",  # Mr
    "Г-ца",  # Mrs
]

IRAN_HONORIFICS= [
    "سید", #Syed/Seyed/Seyyed/Sayyed
    "آقای", #Mr
    "خانم", #Miss/Lady/Madam
    "جناب", #Sir
    "دکترسید", #this is somehow Sayyed combined with Dr
    "دکتر", #the Doctor
    "مهندس", #engineer
    "حجت الاسلام و المسلمین", #honorific title meaning "authority on Islam" or "proof of Islam"
    "حجت‌الاسلام", #honorific title meaning "authority on Islam" or "proof of Islam"
    "آیت‌الله", #title of religious leader (Ayatollah is an honorific title for high ranking Twelver Shia clergy in Iran and Iraq)
    "مهندس سید", #engineer seyed
    
    #ranks
    "سرتیپ پاسدار", #brigadier general 
]

CAMBODIA_HONORIFICS = [
    "បណ្ឌិត",  # Doctor
    "លោកស្រីចៅក្រម",  # Judge
    "ចៅក្រម",  # Judge
    "ឯកឧត្តម",  # His Excellency
    "ឯ.ឧ.",  # E.g.(Exempli Gratia-abbreviation used to introduce examples in a sentence)
    "លោក",  # Mr./Sir
    "លោកស្រី",  # Mrs./Madam
    "លោកជំទាវ",  # Lok Chumteav (title for high-ranking female officials or the wives of high-ranking ministers or government officials)
]

BANGLADESH_HONORIFICS = [
    "বেগম",  # Begum
    "জনাব",  # Mr
    "মিসেস",  # Mrs
    "মিজ",  # Miz
    "ডক্টর",  # Dr
    "ডাঃ",  # Dr
    "ড",  # Dr
    "মাননীয়",  # Hon (Honorable)
    "প্রকৌ",  # Prof
    "এম.পি.",  # M.P (Member of Parliament)
    "এমপি",  # MP (Member of Parliament)
    "এনডিসি",  # NDC (National Defense College/Course)
    "TPr",  # Registered Town Planner (if found in name)
]

HONORIFICS_COUNTRY_MAPPING = {
    "General": DEFAULT_HONORIFICS,
    "Indonesia": INDONESIA_HONORIFICS,
    "Israel": ISRAEL_HONORIFICS,
    "Malaysia": MALAYSIA_HONORIFICS,
    "Nigeria": NIGERIA_HONORIFICS,
    "South Africa": SOUTH_AFRICA_HONORICIS,
    "Thailand": THAILAND_HONORIFICS,
    "Vietnam": VIETNAM_HONORIFICS,
    "Macedonia": MACEDONIA_HONORIFICS,
    "Cambodia": CAMBODIA_HONORIFICS,
    "Bangladesh": BANGLADESH_HONORIFICS,
}


PEP_JOB_TITLES = {
    "ambassador",
    "minister", 
    "charge",
    "high commissioner",
    "nuncio",
    "head",
    "mission",
    "counsel",
    "consul",
    "secretar",
    "attach",
    "assistant",
    "consular agent",
    "honorary",
    "officer",
    "observer",
    "representative",
    "politician",
    "member",
    "membre",
    "miembr",
    "manager",
    "president",
    "chair",
    "judge",
    "chief",
    "ceo",
    "cfo",
    "coo",
    "cmo",
    "cto"
    "vp",
    "deputy",
    "cmd",
    "director",
    "board",
    "vocal",
    "secretar",
    "jefe",
    "jefa",
    "commisioner",
    "addl",
    "dy.",
    "hon",
    "rector",
    "officer",
    "speaker",
    "市长",  #mayor
    "副市长", #vice-mayor
    "委常委", # Member of the Standing Committee
    "部长" # minister
    "书记"  #secretary
    "Baskan", # minister
    "başkan",
    "Üyes", #member
    "পরিচালক",  # director
    "সচিব",  # secretary
    "মন্ত্রী", #minister
}