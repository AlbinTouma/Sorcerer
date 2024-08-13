from nltk.corpus import stopwords
import os
import sys
from pathlib import Path
import pandas as pd
import altair as alt
import json
import nltk
import re
from typing import Optional, Iterable
# Download common English stopwords ie the, at, etc
nltk.download("stopwords")

''''
The code currently doesn't apply the SINGLE_FLAG or NUM_REPEAT_PHONETIC_COMPS_GT3_FLAG to names using CJK characters.
Note that the example thresholds below are those set for People names; there are different thresholds set for the Company names.

source_id;	Entity ID
source_list;	Original source list code
name;	A name from the entity record
name_type;	The type of name: primary, alias or weak alias
NAME_CHARS;	The total number of characters in the name
NAME_COMPS;	The total number of name components when splitting on white space
SEP_COUNT;	The number of separator/delimiter characters that appear; by default these include, :;, |
NUM_REPEAT_NAME_COMPS;	The number of repeated name components
NUM_REPEAT_PHONETIC_COMPS;	The number of phonetic name componets that repeat
NAME_COMPS_GT9_FLAG;	Boolean flag if NAME_COMPS exceeds threshold of 9
NAME_CHARS_GT59_FLAG;	Boolean flag if NAME_CHARS exceeds threshold of 59
SEP_COUNT_GT1_FLAG;	Boolean flag if SEP_COUNT exceeds threshold of 1
NUM_REPEAT_NAME_COMPS_GT3_FLAG;	Boolean flag if NUM_REPEAT_NAME_COMPS exceeds threshold of 3
NUM_REPEAT_PHONETIC_COMPS_GT3_FLAG;	Boolean flag if NUM_REPEAT_PHONETIC_COMPS exceeds threshold of 3
SINGLE_FLAG;	Boolean flag if NAME_COMPS only includes a single name
TOTAL_FLAGS;	Sum of all flags
'''


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

NIGERIA_HONORIFICS = ["alhaji", "alh", "barrister",
                      "barr", "barr.", " FNSE", " SAN", " MNI", " MFR"]
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
    "พล.ท.",  # General
    "พลอากาศเอก",
    "พลอากาศตรี",  # Air Chief Marshal
    "พลเรือเอก",
    "พลเรือตรี",  # Admiral
    "ร้อยโท",
    "พลโท",
    "ว่าที่ร้อยตรี",  # Lieutenant, Acting Lieutenant
    "ร้อยตรี",  # Second Lieutenant
    "พันโท",
    "พันตำรวจตรี",  # Lieutenant Colonel
    "พลตำรวจโท",  # Lieutenant General
    "พันตำรวจโท",  # Police lieutenant colonel
    "พ.ต.อ.",  # Pol. colonel
    "พลตำรวจเอก",  # Police General
    "พลตำรวจตรี",  # Police Major General
    "พันจ่าตรี",  # Major Sergeant(or Chief Petty Officer)
    "พลตรี",
    "พล.ต.ต.",  # Major General
    "ร้อยตำรวจโทหญิง",  # Female Police Lieutenant
    "ร้อยเอก",  # Captain
    "พันจ่าเอก",  # Colonel/Major Sergeant
    "พันเอก",
    "พันตำรวจเอก",  # Colonel
    # Acting Lieutenant Female(or Acting Sub Lieutenant, translation is pretty bad)
    "ว่าที่ร.ต.หญิง",
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
    # ASSISTANT DIRECTOR-GENERAL OF THE ROYAL THAI POLICE  DEPARTMEMT
    "ผู้ช่วยผู้บัญชาการตำรวจแห่งชาติ",
    # DEPUTY DIRECTOR-GENERAL OF THE ROYAL THAI POLICE DEPARTMEMT
    "รองผู้บัญชาการตำรวจแห่งชาติ",
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
    "PGS.TS.",  # Associate Professor Ph.D
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

IRAN_HONORIFICS = [
    "سید",  # Syed/Seyed/Seyyed/Sayyed
    "آقای",  # Mr
    "خانم",  # Miss/Lady/Madam
    "جناب",  # Sir
    "دکترسید",  # this is somehow Sayyed combined with Dr
    "دکتر",  # the Doctor
    "مهندس",  # engineer
    # honorific title meaning "authority on Islam" or "proof of Islam"
    "حجت الاسلام و المسلمین",
    "حجت‌الاسلام",  # honorific title meaning "authority on Islam" or "proof of Islam"
    # title of religious leader (Ayatollah is an honorific title for high ranking Twelver Shia clergy in Iran and Iraq)
    "آیت‌الله",
    "مهندس سید",  # engineer seyed

    # ranks
    "سرتیپ پاسدار",  # brigadier general
]

CAMBODIA_HONORIFICS = [
    "បណ្ឌិត",  # Doctor
    "លោកស្រីចៅក្រម",  # Judge
    "ចៅក្រម",  # Judge
    "ឯកឧត្តម",  # His Excellency
    # E.g.(Exempli Gratia-abbreviation used to introduce examples in a sentence)
    "ឯ.ឧ.",
    "លោក",  # Mr./Sir
    "លោកស្រី",  # Mrs./Madam
    # Lok Chumteav (title for high-ranking female officials or the wives of high-ranking ministers or government officials)
    "លោកជំទាវ",
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
    "MEP",
    "Parliamentarian",
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
    "市长",  # mayor
    "副市长",  # vice-mayor
    "委常委",  # Member of the Standing Committee
    "部长"  # minister
    "书记"  # secretary
    "Baskan",  # minister
    "başkan",
    "Üyes",  # member
    "পরিচালক",  # director
    "সচিব",  # secretary
    "মন্ত্রী",  # minister
}

PEP_JOB_TITLES = {title.lower() for title in PEP_JOB_TITLES}


DEFAULT_SEPARATORS = (",", ":", ";", "\n", "\t", "|")

MULTILINGUAL_STOPWORDS = set()
for lang in ("english", "russian", "chinese", "spanish", "arabic", "french"):
    MULTILINGUAL_STOPWORDS.update(set(stopwords.words(lang)))


def filter_stopwords(text: str, stop_words: set = MULTILINGUAL_STOPWORDS) -> str:
    """Remove stopwords from a supplied text

    Args:
        text (str): text to be processed
        stop_words (set, optional): _description_. Defaults to MULTILINGUAL_STOPWORDS.

    Returns:
        str: filtered text
    """
    text_components = text.split()
    return " ".join([word for word in text_components if word.lower() not in stop_words])


def count_separators(text: str, separators: Optional[Iterable[str]] = None) -> int:
    """Count the occurrences of the separator characters in the input text.

    Args:
        text (str): The input text to search for separator characters.
        separators (Optional[Iterable[str]]): An iterable of separator characters to search for in the input text. Defaults to a tuple containing only the comma character (',') if no value is provided.

    Returns:
        int: The number of times a separator character is found in the input text.

    Examples:
        >>> count_separators("apple, banana, cherry")
        2

        >>> count_separators("apple; banana; cherry, pineapple", separators=[";", ","])
        3
    """
    if separators is None:
        separators = DEFAULT_SEPARATORS

    pattern = fr"{'|'.join(map(re.escape, separators))}"
    characters = re.findall(pattern, text)

    return len(characters)


def count_repeat_components(text: str, strip_stopwords: bool = True) -> int:
    """
    Count the number of repeated components in a given text.

    Args:
        text (str): The input text to be analyzed for repeated components.
        strip_stopwords (bool): choose whether to strip out stopwords, defaults to True
    Returns:
        int: The number of repeated components in the input text.

    Example:
        >>> text = "This is an example example text with repeated repeated components."
        >>> count_repeat_components(text)
        2
    """
    if strip_stopwords:
        text = filter_stopwords(text)
    components = text.lower().split()
    repeat_comps = len(components) - len(set(components))
    return repeat_comps


def detect_honorifics(text: str) -> bool:
    """Compare a text string to our list of honorifics return True if any honorific appears"""
    exclude_countries = {
        "Indonesia", "Vietnam"}  # Don't use these honorifics for now - lots of false posititves from short titles
    honorific_set = {word.lower() for k, v in HONORIFICS_COUNTRY_MAPPING.items(
    ) if k not in exclude_countries for word in v}
    text = text.lower()

    pattern = r'\b(?:' + '|'.join(re.escape(word)
                                  for word in honorific_set) + r')\b'
    if re.search(pattern, text):
        return True

    return False


def detect_pep_job_title(text: str) -> bool:
    """Compare a text string to our list of PEP job titles return True if any job title appears"""
    text = text.lower()
    # Use regular expression to match job titles as standalone words
    for title in PEP_JOB_TITLES:
        pattern = r'\b' + re.escape(title) + r'\b'
        if re.search(pattern, text):
            return True


def detect_cjk_chars(text: str) -> bool:
    """Check to see if cjk chars are present in the text"""

    if re.search("[\uac00-\ud7a3]", text):
        detection = True  # ko
    elif re.search("[\u3040-\u30ff]", text):
        detection = True  # ja
    elif re.search("[\u4e00-\u9FFF]", text):
        detection = True  # zh
    else:
        detection = False

    return detection


def process_pep_name(name: str, separators: Optional[tuple[str]] = None) -> dict:
    """
    Process a PEP's name and generate a dictionary of results.

    Args:
        name (str): The input name to be processed.
        separators (Optional[tuple[str]], optional): A tuple of separator characters used to split name components.
            If not provided, the default separators (",", ":", ";", "/", "\n", "\t") will be used. Default is None.

    Returns:
        dict: A dictionary containing the following keys:
            - "name": The input name
            - "NAME_CHARS": The number of characters in the input name
            - "NAME_COMPS": The number of name components after splitting by separators
            - "SEP_COUNT": The number of separator occurrences in the input name
            - "NUM_REPEAT_NAME_COMPS": The number of repeated components in the input name
            - "NUM_REPEAT_PHONETIC_COMPS": The number of repeated components in the input name after phonetic normalization
    """

    if separators is None:
        separators = DEFAULT_SEPARATORS

    results_dict = {
        "name": name,
        "NAME_CHARS": len(name),
        "NAME_COMPS": len(name.split()),
        "SEP_COUNT": count_separators(name, separators=separators),
        "NUM_REPEAT_NAME_COMPS": count_repeat_components(name, strip_stopwords=False),
        "HONORIFIC_PRESENT": detect_honorifics(name),
        "JOB_TITLE_PRESENT": detect_pep_job_title(name)
    }
    return results_dict


THRESHOLDS_GT = {
    "NAME_COMPS": 9,
    "NAME_CHARS": 59,
    "SEP_COUNT": 1,
    "NUM_REPEAT_NAME_COMPS": 3,

}

THRESHOLDS_EQ = {
    "NAME_COMPS": 1,
}

BOOL_FLAGS = {
    "HONORIFIC_PRESENT": True,
    "JOB_TITLE_PRESENT": True
}

thresholds = {
    "THRESHOLDS_GT": THRESHOLDS_GT,
    "THRESHOLDS_EQ": THRESHOLDS_EQ,
    "BOOL_FLAGS": BOOL_FLAGS
}


def set_name_flags(name_df: pd.DataFrame, thresholds: dict[dict[str, int]]) -> pd.DataFrame:
    """
    Flags values in a pandas DataFrame based on given thresholds.

    This function takes a pandas DataFrame `name_df` and a dictionary of thresholds `thresholds`,
    and creates boolean flags in the DataFrame based on the specified thresholds. The flags are
    created as additional columns in the DataFrame using the `.assign()` method, and the resulting
    DataFrame with the flags is returned.

    Args:
        name_df (pd.DataFrame): The input DataFrame to be flagged.
        thresholds (dict[dict[str, int]]): A dictionary of thresholds for flagging, with keys
            "THRESHOLDS_GT" and "THRESHOLDS_EQ" for greater-than and equal-to checks, respectively.
            The values are inner dictionaries with keys as column names in `name_df` and values
            as threshold values for flagging.

    Returns:
        pd.DataFrame: The input DataFrame `name_df` with additional columns for the flags created
            based on the specified thresholds.

    Example:
            A  B  A_GT2_FLAG  B_EQ5_FLAG  TOTAL_FLAGS
        0  1  4        False       False             0
        1  2  5        False        True             1
         2  3  6         True       False             1
    """

    flag_names = []

    # Greater-than checks
    thresh = thresholds.get("THRESHOLDS_GT", {})
    for k, v in thresh.items():
        flag_name = f"{k.upper()}_GT{v}_FLAG"
        name_df = name_df.assign(**{flag_name: name_df[k] > v})
        flag_names.append(flag_name)
        if "REPEAT_PHONETIC_COMPS" in k:
            phonetic_name_flag_name = flag_name
        else:
            phonetic_name_flag_name = False

    thresh = thresholds.get("THRESHOLDS_EQ", {})
    for k, v in thresh.items():
        if v == 1 and not isinstance(v, bool):
            flag_name = "SINGLE_FLAG"
        else:
            flag_name = f"{k.upper()}_EQ{v}_FLAG"

        name_df.loc[:, flag_name] = name_df.loc[:, k] == v
        flag_names.append(flag_name)

    thresh = thresholds.get("BOOL_FLAGS", {})
    for k, v in thresh.items():
        flag_name = f"{k.upper()}_FLAG"
        name_df.loc[:, flag_name] = name_df.loc[:, k] == v
        # name_df.loc[:, flag_name] = name_df.loc[:, k].astype(int)
        flag_names.append(flag_name)

    # Ignore CJK char names for SINGLE_FLAG col
    cjk_names_flag = name_df.loc[:, "name"].map(detect_cjk_chars)
    if "SINGLE_FLAG" in name_df.columns:
        name_df.loc[:, "SINGLE_FLAG"] = name_df.loc[:,
                                                    "SINGLE_FLAG"] * ~cjk_names_flag
    # Ignore phoneitc repeats in CJK char names
    if phonetic_name_flag_name:
        name_df.loc[:, phonetic_name_flag_name] = name_df.loc[:,
                                                              phonetic_name_flag_name] * ~cjk_names_flag

    name_df.loc[:, flag_names] = name_df[flag_names].applymap(int)

    name_df.loc[:, "TOTAL_FLAGS"] = name_df.loc[:, flag_names].sum(axis=1)

    return name_df


def execute_name_completeness(df):

    if '_source.data.names.primary_name' in df.columns:
        # Convert array to strings
       # df['_source.data.names.primary_name'] = df['_source.data.names.primary_name'].apply(
       #     lambda x: ', '.join(map(str, x)))

        # Apply process_pep_name to each row and save as Series of dictionaries in Result
        result = df['_source.data.names.primary_name'].apply(
            lambda x: process_pep_name(x))

    # Normalise the result to get df
        result = pd.json_normalize(result)

    # Concatenate the results into df
        df = pd.concat([df, result], axis=1)

    # Call the set_name_flags to flag issues with name column
        df = set_name_flags(df, thresholds)

        return df


def main(file_path, parquet_file):
    df = pd.read_parquet(f'{file_path}')
    if not df.empty:
        df = execute_name_completeness(df)
        df.to_parquet(f'parquet/{parquet_file}')
        return df


if __name__ == "__main__":
    df = main()
