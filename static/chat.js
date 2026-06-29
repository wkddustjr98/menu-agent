const chatBox = document.getElementById("chat-box");
const input = document.getElementById("message-input");
const button = document.getElementById("send-btn");

const MENU_API_URL = "https://mc.skhystec.com/V3/prc/selectMenuList.prc";

let currentMenus = [];
let currentQuery = {};
let chatHistory = [];

const CAMPUSES = {
    "이천": "IC",
    "청주": "CJ",
    "분당": "BD"
};

const CAFETERIAS = {
    "r&d": { campus: "IC", seq: "10" },
    "rnd": { campus: "IC", seq: "10" },
    "sky": { campus: "IC", seq: "7" },
    "스카이": { campus: "IC", seq: "7" },
    "복지관": { campus: "IC", seq: "2" },
    "복지": { campus: "IC", seq: "2" },
    "p&t4": { campus: "IC", seq: "9" },
    "피앤티": { campus: "IC", seq: "9" },
    "중앙": { campus: "IC", seq: "1" },
    "청운": { campus: "IC", seq: "3" },
    "행복1": { campus: "IC", seq: "4" },
    "행복2": { campus: "IC", seq: "6" },
    "1캠": { campus: "CJ", seq: "11" },
    "1캠퍼스": { campus: "CJ", seq: "11" },
    "2캠": { campus: "CJ", seq: "12" },
    "2캠퍼스": { campus: "CJ", seq: "12" },
    "3캠": { campus: "CJ", seq: "13" },
    "3캠퍼스": { campus: "CJ", seq: "13" },
    "4캠": { campus: "CJ", seq: "16" },
    "4캠퍼스": { campus: "CJ", seq: "16" },
    "기숙사": { campus: "CJ", seq: "14" },
    "청주기숙사": { campus: "CJ", seq: "14" },
    "비원": { campus: "BD", seq: "21" },
    "n타워": { campus: "BD", seq: "26" },
    "두산": { campus: "BD", seq: "22" },
    "두산타워": { campus: "BD", seq: "22" },
    "센터원": { campus: "BD", seq: "24" }
};

const MEALS = {
    "아침": "BF",
    "조식": "BF",
    "점심": "LN",
    "중식": "LN",
    "저녁": "DN",
    "석식": "DN",
    "야식": "SN"
};

button.addEventListener("click", sendMessage);

input.addEventListener("keydown", function (e) {
    if (e.key === "Enter") sendMessage();
});

function addUserMessage(text) {
    const div = document.createElement("div");
    div.className = "user-message";
    div.innerText = text;
    chatBox.appendChild(div);
    scrollBottom();
}

function addBotMessage(html) {
    const div = document.createElement("div");
    div.className = "bot-message";
    div.innerHTML = html;
    chatBox.appendChild(div);
    scrollBottom();
}

function showLoading() {
    const div = document.createElement("div");
    div.className = "bot-message loading";
    div.id = "loading";
    div.innerHTML = "🤖 처리 중입니다...";
    chatBox.appendChild(div);
    scrollBottom();
}

function removeLoading() {
    const loading = document.getElementById("loading");
    if (loading) loading.remove();
}

function scrollBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

function todayYmd(offset = 0) {
    const d = new Date();
    d.setDate(d.getDate() + offset);

    const y = d.getFullYear();
    const m = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");

    return `${y}${m}${day}`;
}

function parseMessage(message) {
    const lower = message.toLowerCase();

    let result = {
        campus: null,
        cafeteriaSeq: null,
        mealType: null,
        ymd: null,
        hasMenuInfo: false
    };

    for (const [name, code] of Object.entries(CAMPUSES)) {
        if (lower.includes(name.toLowerCase())) {
            result.campus = code;
            result.hasMenuInfo = true;
        }
    }

    for (const [alias, info] of Object.entries(CAFETERIAS)) {
        if (lower.includes(alias.toLowerCase())) {
            result.cafeteriaSeq = info.seq;
            result.campus = result.campus || info.campus;
            result.hasMenuInfo = true;
        }
    }

    for (const [name, code] of Object.entries(MEALS)) {
        if (lower.includes(name)) {
            result.mealType = code;
            result.hasMenuInfo = true;
        }
    }

    if (lower.includes("모레")) {
        result.ymd = todayYmd(2);
        result.hasMenuInfo = true;
    } else if (lower.includes("내일")) {
        result.ymd = todayYmd(1);
        result.hasMenuInfo = true;
    } else {
        result.ymd = todayYmd(0);
    }

    return result;
}

function formatMenus(rawMenus) {
    return rawMenus.map(m => ({
        course: m.COURSE_NAME || "",
        main: m.MENU_NAME || "",
        sides: [
            m.SIDE_1 || "",
            m.SIDE_2 || "",
            m.SIDE_3 || "",
            m.SIDE_4 || "",
            m.SIDE_5 || "",
            m.SIDE_6 || ""
        ].filter(x => x.trim() !== ""),
        kcal: m.KCAL || "",
        rating: Number(m.AVG_STAR || 0),
        rating_count: Number(m.SATI_CNT || 0),
        origin: m.MENU_ORIGIN || "",
        soldout: m.SOLDOUT_YN === "Y",
        congestion: m.CONGESTION || "",
        guide: m.MENU_GUIDE || ""
    }));
}

async function fetchMenus(query) {
    const body = new URLSearchParams();

    body.append("campus", query.campus);
    body.append("cafeteriaSeq", query.cafeteriaSeq);
    body.append("mealType", query.mealType);
    body.append("ymd", query.ymd);

    const response = await fetch(MENU_API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: body.toString()
    });

    const data = await response.json();

    return formatMenus(data.menuList || []);
}

function createMenuCard(menu) {
    let sides = "";

    for (const side of menu.sides || []) {
        sides += `<li>${side}</li>`;
    }

    const soldout = menu.soldout ? "❌ 품절" : "🟢 판매중";

    return `
        <div class="menu-card">
            <div class="menu-title">🍽 ${menu.course}</div>

            <div><b>${menu.main}</b></div>
            <br>

            ⭐ ${menu.rating} (${menu.rating_count})
            <br>

            🔥 ${menu.kcal || "-"} kcal
            <br>

            ${soldout}
            <br><br>

            <b>반찬</b>
            <ul>${sides}</ul>

            <br>
            <small>${menu.origin}</small>
        </div>
    `;
}

function renderMenuResponse(menus, query) {
    let html = "";

    html += `<b>📅 ${query.ymd}</b><br>`;
    html += `<b>식사:</b> ${query.mealType}<br><br>`;

    if (!menus || menus.length === 0) {
        html += "조회된 메뉴가 없습니다.";
        return html;
    }

    for (const menu of menus) {
        html += createMenuCard(menu);
    }

    return html;
}

function renderRecommendResponse(answer) {
    return `
        <div class="recommend-box">
            <b>🤖 AI 답변</b><br><br>
            ${answer.replace(/\n/g, "<br>")}
        </div>
    `;
}

async function askAI(message) {
    const response = await fetch("/api/recommend", {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            message: message,
            menus: currentMenus,
            history: chatHistory
        })
    });

    const result = await response.json();

    if (!result.success) {
        throw new Error(result.message);
    }

    chatHistory = result.data.history || chatHistory;

    return result.data.recommendation;
}

async function sendMessage() {
    const message = input.value.trim();

    if (message === "") return;

    addUserMessage(message);
    input.value = "";
    showLoading();

    try {
        const parsed = parseMessage(message);

        if (parsed.hasMenuInfo) {
            currentQuery = {
                campus: parsed.campus || currentQuery.campus,
                cafeteriaSeq: parsed.cafeteriaSeq || currentQuery.cafeteriaSeq,
                mealType: parsed.mealType || currentQuery.mealType || "LN",
                ymd: parsed.ymd || currentQuery.ymd || todayYmd(0)
            };

            if (!currentQuery.campus) {
                removeLoading();
                addBotMessage("어느 캠퍼스인가요?<br>(이천 / 청주 / 분당)");
                return;
            }

            if (!currentQuery.cafeteriaSeq) {
                removeLoading();
                addBotMessage("어느 식당인가요?");
                return;
            }

            currentMenus = await fetchMenus(currentQuery);
            chatHistory = [];

            removeLoading();
            addBotMessage(renderMenuResponse(currentMenus, currentQuery));
            return;
        }

        if (currentMenus.length === 0) {
            removeLoading();
            addBotMessage("먼저 메뉴를 조회해주세요.<br>예: SKY 점심");
            return;
        }

        const answer = await askAI(message);

        removeLoading();
        addBotMessage(renderRecommendResponse(answer));
    }

    catch (e) {
        removeLoading();
        console.error(e);
        addBotMessage("❌ " + e.message);
    }
}