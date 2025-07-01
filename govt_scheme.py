# govt_scheme.py

def get_central_schemes():
    """
    Returns a list of dictionaries with detailed info about central government
    financial schemes for street vendors.
    """
    schemes = [
        {
            "name": "PM SVANidhi (Pradhan Mantri Street Vendor’s AtmaNirbhar Nidhi)",
            "description": (
                "A flagship scheme by the Ministry of Housing and Urban Affairs "
                "(MoHUA) offering affordable collateral-free working capital loans "
                "to street vendors. The loans start at ₹10,000 and can be incrementally "
                "enhanced up to ₹50,000 upon timely repayment. Vendors also receive a "
                "7% interest subsidy annually and cashback incentives on digital payments."
            ),
            "features": [
                "Initial loan amount: ₹10,000 with possible enhancement to ₹20,000 and ₹50,000",
                "7% annual interest subsidy to reduce loan cost",
                "Cashback up to ₹1,200 for digital transactions to encourage digital payments",
                "Open to registered urban street vendors under the Street Vendors Act, 2014"
            ],
            "link": "https://pmsvanidhi.mohua.gov.in/"
        },
        {
            "name": "MUDRA Yojana (Micro Units Development and Refinance Agency)",
            "description": (
                "Provides small loans up to ₹50,000 to micro and small enterprises including "
                "street vendors to help start or expand businesses without collateral."
            ),
            "features": [
                "Shishu category loans up to ₹50,000",
                "No collateral required",
                "Accessible through banks and NBFCs"
            ],
            "link": "https://mudra.org.in/"
        },
        {
            "name": "DAY-NULM (Deendayal Antyodaya Yojana - National Urban Livelihoods Mission)",
            "description": (
                "Provides skill development, capacity building, and support for urban street "
                "vendors to improve their livelihoods. It also assists in forming vendor "
                "committees and improving vending infrastructure."
            ),
            "features": [
                "Skill training and capacity building",
                "Provision of vending ID cards and registration",
                "Support for infrastructure like carts, stalls, and vending zones"
            ],
            "link": "https://aajeevika.gov.in/content/day-nulm"
        }
    ]
    return schemes


def get_state_scheme(state_name):
    """
    Takes the name of a state (string) and returns a dictionary containing detailed info
    about the state-specific vendor financial scheme or its adoption of PM SVANidhi.
    """
    state_schemes = {
        "Andhra Pradesh": {
            "state": "Andhra Pradesh",
            "has_own_scheme": True,
            "scheme_name": "Jagananna Thodu",
            "description": (
                "Provides an interest-free working capital loan of ₹10,000 to street vendors "
                "and artisans. The Andhra Pradesh government fully pays the interest, "
                "making it easier for vendors to access funds. The scheme works in tandem "
                "with the central PM SVANidhi scheme and is disbursed via ward/village secretariats."
            ),
            "link": "https://www.navasakam.ap.gov.in/"
        },
        "Madhya Pradesh": {
            "state": "Madhya Pradesh",
            "has_own_scheme": True,
            "scheme_name": "Mukhyamantri Street Vendor Loan Yojana",
            "description": (
                "Offers an interest-free loan of ₹10,000 to registered street vendors. "
                "The scheme is managed by municipal bodies and encourages repeat loans "
                "upon timely repayment, supporting vendors’ financial sustainability."
            ),
            "link": "https://urban.mp.gov.in/"
        },
        "Odisha": {
            "state": "Odisha",
            "has_own_scheme": True,
            "scheme_name": "Urban Vendor Livelihood Scheme (Under DAY-NULM)",
            "description": (
                "Odisha provides financial and infrastructure support to street vendors, "
                "including a ₹6,000 direct cash assistance during the COVID-19 pandemic to "
                "registered vendors. The state also facilitates vendor registration, training, "
                "and vending infrastructure development."
            ),
            "link": "https://sudawb.org/Program-Details/11"
        },
        "West Bengal": {
            "state": "West Bengal",
            "has_own_scheme": False,
            "scheme_name": None,
            "description": (
                "West Bengal currently does not have a separate state-specific financial loan "
                "scheme for street vendors. The state strongly implements the central PM SVANidhi "
                "scheme, with over 1.8 lakh vendors benefitting. Vendor registration and vending "
                "regulations are managed under the West Bengal Street Vendors (Protection) Rules, 2018."
            ),
            "link": "https://sudawb.org/Program-Details/11"
        },
        "Bihar": {
            "state": "Bihar",
            "has_own_scheme": False,
            "scheme_name": None,
            "description": (
                "Bihar does not have a separate vendor loan scheme. It actively implements "
                "the central PM SVANidhi scheme through urban local bodies, providing vendor "
                "registration and awareness drives but no additional state-funded loan."
            ),
            "link": "http://urban.bih.nic.in/"
        },
        "Uttar Pradesh": {
            "state": "Uttar Pradesh",
            "has_own_scheme": False,
            "scheme_name": None,
            "description": (
                "Uttar Pradesh primarily follows the central PM SVANidhi scheme for street vendors. "
                "The state supplements it with awareness campaigns, brand ambassadors, free health "
                "camps, and vendor ID issuance. There is no separate state-funded financial scheme."
            ),
            "link": "https://upurban.gov.in/"
        }
    }

    # Normalize input for case insensitive matching
    state_key = state_name.strip().title()
    return state_schemes.get(state_key, {
        "state": state_name,
        "has_own_scheme": False,
        "scheme_name": None,
        "description": "Information about this state's vendor schemes is not available currently.",
        "link": None
    })
