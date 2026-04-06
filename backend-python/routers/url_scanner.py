from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
from urllib.parse import urlparse
from tld import get_tld  # this is usefull for get top level domain from any url
import re
import shap


# Create the router
router = APIRouter()

try:
    print("Loading URL Model and SHAP Explainer...")
    model = joblib.load("models/url_model.joblib")
    explainer = shap.TreeExplainer(model)
    print("AI Engine Ready.")
except Exception as e:
    print(f"Warning: Could not load URL model. Error: {e}")


# ? Feature Engineering.

# Since an AI cannot just "read" a URL and understand it like a human, data scientists have to write mini-programs (functions) to extract specific, mathematical clues from the text. The AI then uses these clues to make its decision.


# If a URL uses an IP address instead of a standard word-based domain name,
# it is a massive red flag.
# This feature simply asks the question: "Does this URL contain an IP address? Yes or No?"
def having_ip_address(url):

    match = re.search(
        "(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\."
        "([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|"  # IPv4
        "((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)"  # IPv4 in hexadecimal
        "(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}",
        url,
    )  # Ipv6

    if match:
        return 1
        # means ip address found in url
    else:
        return 0
        # means ip address not found in url


# A normal, safe website usually only has one or two dots (e.g., google.com or www.google.com).
# Scammers try to trick people by creating crazy "subdomains" to make the link look official.
# A fake PayPal link might look like this: login.update.secure.paypal.com.scamwebsite.net
# If the AI sees a URL with 5 or 6 dots, it will immediately flag it as highly suspicious!


def count_dots(url):
    count_dot = url.count(".")
    return count_dot


# This is one of the oldest phishing tricks in the book!
# Web browsers are programmed to ignore everything before an @ symbol in a URL.
# If a scammer sends you http://www.google.com@scam-website.com,
# your human eyes see "https://www.google.com/search?q=google.com",
# but your browser ignores it and takes you straight to scam-website.com.
# Legitimate websites almost never use the @ symbol in their URLs.
# If your AI sees one, it is a huge red flag!


def count_atrate(url):
    count = url.count("@")
    return count


# Normal websites try to keep their pages easy to find,
# so they usually only have one or two folders
#  (like amazon.com/electronics/phones).
#  Scammers hide their fake login pages deep inside
#  complex folder structures on hacked servers.
#  If a URL looks like site.com/wp-admin/includes/temp/data/login/user/verify.php
#   (which has 7 slashes), the AI will get very suspicious.


def no_of_dir(url):
    urldir = urlparse(url).path
    count = urldir.count("/")
    return count


# Double slashes belong at the very beginning of a URL (http://).
# They should never be in the middle of the path. If they are in the middle,
# it usually means the scammer is trying to embed a second,
# hidden website inside the first one (an "open redirect" attack).


def no_of_embed(url):
    urldir = urlparse(url).path
    count = urldir.count("//")
    return count


# Scan the URL. Does it contain the text 'bit.ly' OR 'goo.gl' OR 'tinyurl' OR 't.co'?" *
# The giant block of red text is just a massive list of the most popular URL shortening
# services on the internet. The | symbol simply means "OR" in Regex.
# If you find any of those famous shortener names hiding in the URL, flag it with a 1.
# If it looks like a normal, full-length URL, give it a 0


def shortening_service(url):
    match = re.search(
        "bit\\.ly|goo\\.gl|shorte\\.st|go2l\\.ink|x\\.co|ow\\.ly|t\\.co|tinyurl|tr\\.im|is\\.gd|cli\\.gs|"
        "yfrog\\.com|migre\\.me|ff\\.im|tiny\\.cc|url4\\.eu|twit\\.ac|su\\.pr|twurl\\.nl|snipurl\\.com|"
        "short\\.to|BudURL\\.com|ping\\.fm|post\\.ly|Just\\.as|bkite\\.com|snipr\\.com|fic\\.kr|loopt\\.us|"
        "doiop\\.com|short\\.ie|kl\\.am|wp\\.me|rubyurl\\.com|om\\.ly|to\\.ly|bit\\.do|t\\.co|lnkd\\.in|"
        "db\\.tt|qr\\.ae|adf\\.ly|goo\\.gl|bitly\\.com|cur\\.lv|tinyurl\\.com|ow\\.ly|bit\\.ly|ity\\.im|"
        "q\\.gs|is\\.gd|po\\.st|bc\\.vc|twitthis\\.com|u\\.to|j\\.mp|buzurl\\.com|cutt\\.us|u\\.bb|yourls\\.org|"
        "x\\.co|prettylinkpro\\.com|scrnch\\.me|filoops\\.info|vzturl\\.com|qr\\.net|1url\\.com|tweez\\.me|v\\.gd|"
        "tr\\.im|link\\.zip\\.net",
        url,
    )
    if match:
        return 1
    else:
        return 0


# The "Cheap Scam" Clue: Setting up a secure https connection used to cost money and require verification.
# While it is easier today, many lazy hackers still set up quick, temporary phishing sites using the unsecure http.
# If your model sees 0 for https and 1 for http, it might get a little suspicious.
# The "Hidden Redirect" Trick (The Main Reason): A normal, safe URL will only have http or https exactly one time at the very beginning.
# However, hackers love to hide a second link inside the main link to forcefully redirect you.


def count_https(url):
    count = url.count("https")
    return count


def count_http(url):
    count = url.count("http")
    return count


# This section is adding the final "Symbol Counters" and a very important "Length Tracker."
# Just like the @ symbol, hackers use these specific characters to disguise their true intentions.


def count_per(url):
    return url.count("%")


def count_ques(url):
    return url.count("?")


def count_hyphen(url):
    return url.count("-")


def count_equal(url):
    return url.count("=")


def length_of_url(url):
    return len(url)


# Uses the urlparse tool to grab just the netloc (network location/hostname) and
# measures its length.


def hostname_length(url):
    return len(urlparse(url).netloc)


# Uses the super-search Regex tool (re.search) to scan
# the URL against a hardcoded list of famous scam words.
def suspicious_word(url):

    match = re.search(
        "PayPal|login|signin|bank|account|update|free|lucky|service|bonus|ebayisapi|webscr",
        url,
    )

    if match:
        return 1
    else:
        return 0


# It looks at every single character in the URL one by one and asks, "Are you a number? (isnumeric)".
# It keeps a running tally of how many numbers it finds.
def digit_count(url):
    digits = 0

    for i in url:
        if i.isnumeric():
            digits += 1

    return digits


# Just like the number counter, it loops through the text and asks,
# "Are you a letter of the alphabet? (isalpha)".
def letter_count(url):
    letter = 0

    for i in url:
        if i.isalpha():
            letter += 1

    return letter


# A normal website usually has simple, short folder names like amazon.com/electronics/phones. Hackers,
# however, often auto-generate massive, random folder names to hide their malicious files
#  (e.g., scam.com/x990234abdf90234/login). Measuring the length of that very first folder is a great way to catch them.


def fd_length(url):
    urlpath = urlparse(url).path
    try:
        return len(urlpath.split("/")[1])
    except:
        return 0


# Feature 2: Length of Top Level Domain
# This creates a temporary text column first

# The TLD is the extension at the very end of the main website name (like .com, .org, or .in).
# Normal websites use standard extensions that are usually 2 to 4 letters long.
# Scammers often use cheap, obscure, or highly unusual extensions.


def tld_length(tld):
    try:
        return len(tld)
    except:
        return -1


# --- THE TRANSLATOR ---
# This converts our ugly code variables into beautiful English sentences for the React frontend!
feature_translations = {
    "count_of_dir": "The link contains an unusually high number of hidden folders.",
    "fd_length": "The folder names in this link are suspiciously long.",
    "length_of_url": "The overall web address is suspiciously long, often used to hide the true destination.",
    "count_of_dots": "Too many dots are used, which is a common trick to create fake subdomains.",
    "use_of_ip": "The link uses a raw IP address instead of a standard trusted domain name.",
    "sus_url": 'The link contains common scam words (like "login", "update", or "paypal").',
    "count-digits": "The link contains an unusually high number of random numbers.",
    "count-letters": "The text structure of the link looks artificially generated.",
    "count_https": "The security certificate structure is highly unusual.",
    "short_url": "This is a shortened link (like bit.ly) which hides the final destination.",
    "count_of_hyphen": "There are too many hyphens, often used to fake real brand names.",
    "count_of_atrate": 'The presence of "@" symbols can redirect users to a different destination, often used in phishing attacks.',
    "count_of_embed": 'The link contains embedded elements (like "//" or unusual structures) that may hide the actual destination.',
    "count_http": "The link uses insecure HTTP protocol instead of HTTPS, which may indicate a lack of security.",
    "count_%": 'The URL contains encoded characters ("%"), often used to obfuscate malicious links.',
    "count_?": 'Too many query parameters ("?") can be used to confuse users or hide malicious intent.',
    "count_=": 'Multiple "=" signs in parameters may indicate complex or suspicious data manipulation in the URL.',
    "hostname_length": "The domain name is unusually long, which is often used to mimic legitimate websites.",
    "tld_length": "The top-level domain (like .com, .xyz) is unusually long or uncommon, which can be suspicious.",
}


def extract_features(url):

    url = str(url)
    print(f"Scanning URL: {url}\n" + "-" * 30)

    # 1. Extract the TLD first (needed for the tld_length feature)
    tld_str = get_tld(url, fail_silently=True)

    # 2. Build a dictionary with all 20 features in the EXACT order of your X variables
    # We use your pre-defined functions and some built-in Python string counters
    features = pd.Series(
        {
            "use_of_ip": having_ip_address(url),
            "count_of_dots": count_dots(url),
            "count_of_atrate": count_atrate(url),
            "count_of_dir": no_of_dir(url),
            "count_of_embed": no_of_embed(url),
            "short_url": shortening_service(url),
            "count_https": count_https(url),
            "count_http": count_http(url),
            "count_%": count_per(url),
            "count_?": count_ques(url),
            "count_of_hyphen": count_hyphen(url),
            "count_=": count_equal(url),
            "length_of_url": length_of_url(url),
            "hostname_length": hostname_length(url),
            "sus_url": suspicious_word(url),
            "count-digits": digit_count(url),
            "count-letters": letter_count(url),
            "fd_length": fd_length(url),
            "tld_length": tld_length(tld_str),
        }
    )

    return features


# Define the expected input from Node.js
class URLInput(BaseModel):
    url: str


# ? The actual API Endpoint
@router.post("/analyze-url")
def analyze_url(data: URLInput):
    target_url = data.url
    print(f"Python received this URL: {target_url}")

    # --- STEP 1: THE WHITELIST (The Production Fix) ---
    # List the core domains of massive tech companies that have complex, messy URLs
    trusted_domains = [
        "youtube.com",
        "google.com",
        "amazon.com",
        "wikipedia.org",
        "linkedin.com",
        "github.com",
    ]

    # Check if any trusted domain is inside the URL
    if any(trusted in target_url.lower() for trusted in trusted_domains):
        return {"threat_level": "Safe", "reason": "Safe: Verified Trusted Domain"}

    # --- STEP 2: THE AI PIPELINE ---

    try:
        # Extract the 19 features
        features_series = extract_features(target_url)

        # Convert to a 2D DataFrame for the ML model
        input_df = pd.DataFrame([features_series.to_dict()])

        # make the prediction
        prediction = model.predict(input_df)

        # Map the ML result (1 = Threat, 0 = Safe) to your React UI logic
        if prediction[0] == 0:
            return {
                "threat_level": "Safe",
                "reason": "No suspicious patterns or hidden tricks detected in the link structure.",
            }
        else:
            # --- If Fake, wake up the SHAP Detective! and find the features which makes the prediction as fake---
            shap_values = explainer(input_df)

            # Get the explanation for the "Fake" class (Class 1)
            fake_explanation = shap_values[:, :, 1][0]

            # Zip the feature names and their math scores together into a list
            feature_impacts = list(
                zip(fake_explanation.feature_names, fake_explanation.values)
            )

            # THE EXTRACTOR: Filter only the RED bars (scores greater than 0)
            red_flags = [item for item in feature_impacts if item[1] > 0]

            # Sort them so the biggest red bar is at the top of the list!
            red_flags.sort(key=lambda x: x[1], reverse=True)

            # Grab the top 3 biggest red bars
            top_3_red_flags = red_flags[:3]

            # Format the top 3 reasons with bullet points so React can display them easily
            final_reasons_list = []

            for flag in top_3_red_flags:
                feature_name = flag[0]

                english_reason = feature_translations.get(
                    feature_name, f"Suspicious activity detected in: {feature_name}"
                )

                final_reasons_list.append(f"• {english_reason}")

            # Join the bullet points together with line breaks
            #Python backend is sending a string with line breaks, like this: "• Reason 1\n• Reason 2\n• Reason 3"
            combined_reason = "\n".join(final_reasons_list)

            return {
                "threat_level": "High", 
                "reason": combined_reason
                }

    except Exception as e:
        print(f"Extraction Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error analyzing URL features.")
