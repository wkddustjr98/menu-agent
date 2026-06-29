"""
프로젝트 전체에서 사용하는 설정

- 회사 API 주소
- 캠퍼스 코드
- 식당 코드
- 식사 코드
"""

API_URL = "https://mc.skhystec.com/V3/prc/selectMenuList.prc"


# ----------------------------------------
# Campus
# ----------------------------------------

CAMPUSES = {
    "이천": "IC",
    "청주": "CJ",
    "분당": "BD"
}


# ----------------------------------------
# Cafeteria
# aliases에는 사용자가 입력할 수 있는 표현을 모두 넣는다.
# seq는 회사 API의 cafeteriaSeq
# ----------------------------------------

CAFETERIAS = {
    "R&D": {
        "campus": "IC",
        "seq": "10",
        "aliases": [
            "r&d",
            "rnd",
            "R&D"
        ]
    },
    "SKY": {
        "campus": "IC",
        "seq": "7",
        "aliases": [
            "sky",
            "SKY",
            "스카이"
        ]
    },
    "복지관": {
        "campus": "IC",
        "seq": "2",
        "aliases": [
            "복지",
            "복지관",
            "복지관"
        ]
    },
    "P&T4": {
        "campus": "IC",
        "seq": "9",
        "aliases": [
            "피앤티",
            "P&T",
            "피앤티4",
            "P&T4"
            
        ]
    },

    "중앙": {
        "campus": "IC",
        "seq": "1",
        "aliases": [
            "중앙",
            "center"
        ]
    },

    "청운": {
        "campus": "IC",
        "seq": "3",
        "aliases": [
            "청운"
        ]
    },
    "행복1": {
        "campus": "IC",
        "seq": "4",
        "aliases": [
            "행복1"
            
        ]
    },
    "행복2": {
        "campus": "IC",
        "seq": "6",
        "aliases": [
            "행복2"
            
        ]
    },
    "1캠퍼스": {
        "campus": "CJ",
        "seq": "11",
        "aliases": [
            "1캠",
            "1캠퍼스",
            "1camp"
        ]
    },
    "2캠퍼스": {
        "campus": "CJ",
        "seq": "12",
        "aliases": [
            "2캠",
            "2캠퍼스",
            "2camp"
        ]
    },
    "3캠퍼스": {
        "campus": "CJ",
        "seq": "13",
        "aliases": [
            "3캠",
            "3캠퍼스",
            "3camp"
        ]
    },
    "4캠퍼스": {
        "campus": "CJ",
        "seq": "16",
        "aliases": [
            "4캠",
            "4캠퍼스",
            "4camp"
        ]
    },
    "청주기숙사": {
        "campus": "CJ",
        "seq": "14",
        "aliases": [
            "청주기숙사",
            "기숙사"
            
        ]
    },
    "비원(분당캠퍼스)": {
        "campus": "BD",
        "seq": "21",
        "aliases": [
            "비원",
            "분당",
            "분당캠퍼스"
        ]
    },
    "N타워": {
        "campus": "BD",
        "seq": "26",
        "aliases": [
            "N",
            "N타워"
            
        ]
    },
    "두산타워(거점)": {
        "campus": "BD",
        "seq": "22",
        "aliases": [
            "두산",
            "두산타워",
            "두산타워(거점)"
        ]
    },
    "센터원(거점)": {
        "campus": "BD",
        "seq": "24",
        "aliases": [
            "센터",
            "센터원",
            "센터원(거점)"
        ]
    },
}


# ----------------------------------------
# Meal
# ----------------------------------------

MEALS = {
    "아침": "BF",
    "조식": "BF",

    "점심": "LN",
    "중식": "LN",

    "저녁": "DN",
    "석식": "DN"
}