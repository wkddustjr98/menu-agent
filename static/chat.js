const chatBox = document.getElementById("chat-box");
const input = document.getElementById("message-input");
const button = document.getElementById("send-btn");

button.addEventListener("click", sendMessage);

input.addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
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
    if (loading) {
        loading.remove();
    }
}

function scrollBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

function createMenuCard(menu) {
    let sides = "";

    for (const side of menu.sides || []) {
        if (side && side.trim() !== "") {
            sides += `<li>${side}</li>`;
        }
    }

    const soldout = menu.soldout ? "❌ 품절" : "🟢 판매중";

    return `
        <div class="menu-card">
            <div class="menu-title">🍽 ${menu.course || ""}</div>

            <div><b>${menu.main || ""}</b></div>
            <br>

            ⭐ ${menu.rating ?? 0} (${menu.rating_count ?? 0})
            <br>

            🔥 ${menu.kcal || "-"} kcal
            <br>

            ${soldout}
            <br><br>

            <b>반찬</b>
            <ul>${sides}</ul>

            <br>

            <small>${menu.origin || ""}</small>
        </div>
    `;
}

function renderMenuResponse(data) {
    let html = "";

    html += `<b>📅 ${data.query?.ymd || ""}</b><br>`;
    html += `<b>식사:</b> ${data.query?.meal_type || ""}<br><br>`;

    if (!data.menus || data.menus.length === 0) {
        html += "조회된 메뉴가 없습니다.";
        return html;
    }

    for (const menu of data.menus) {
        html += createMenuCard(menu);
    }

    return html;
}

function renderRecommendResponse(data) {
    let html = "";

    html += `
        <div class="recommend-box">
            <b>🤖 AI 답변</b><br><br>
            ${data.recommendation.replace(/\n/g, "<br>")}
        </div>
    `;

    return html;
}

async function sendMessage() {
    const message = input.value.trim();

    if (message === "") {
        return;
    }

    addUserMessage(message);
    input.value = "";

    showLoading();

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            credentials: "same-origin",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message
            })
        });

        const result = await response.json();

        removeLoading();

        if (!result.success) {
            addBotMessage("❌ " + result.message);
            return;
        }

        const data = result.data;

        if (data.type === "ask") {
            addBotMessage(data.question);
            return;
        }

        if (data.type === "menu") {
            addBotMessage(renderMenuResponse(data));
            return;
        }

        if (data.type === "recommend") {
            addBotMessage(renderRecommendResponse(data));
            return;
        }

        addBotMessage("응답 형식을 이해하지 못했습니다.");
    }

    catch (e) {
        removeLoading();
        console.error(e);
        addBotMessage("❌ 서버 오류가 발생했습니다.");
    }
}