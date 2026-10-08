const input = document.getElementById("userInput");
const messages = document.getElementById("messages");

const conversationHistory = [];

async function sendMessage() {
    const text = input.value.trim();

    if (!text) return;

    // Show user's message
    addMessage(text, "user");

    // Clear input
    input.value = "";

    // Disable input while waiting
    input.disabled = true;

    try {
        const response = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: text,
                history: conversationHistory
            })
        });

        if (!response.ok) {
            throw new Error("API request failed");
        }

        const data = await response.json();

        // Show bot response
        addMessage(data.response, "bot");

        // Save conversation
        conversationHistory.push({
            role: "user",
            content: text
        });

        conversationHistory.push({
            role: "assistant",
            content: data.response
        });

        // Show escalation information
        if (data.escalated) {
            addMessage(
                "⚠️ Your request has been escalated to a support specialist.",
                "bot"
            );
        }

    } catch (error) {

        console.error("Chat error:", error);

        addMessage(
            "❌ Sorry, I couldn't connect to the support server.",
            "bot"
        );

    } finally {
        input.disabled = false;
        input.focus();
    }
}


function addMessage(text, sender) {

    const message = document.createElement("div");

    message.className = `message ${sender}`;

    message.textContent = text;

    messages.appendChild(message);

    // Scroll to bottom
    messages.scrollTop = messages.scrollHeight;
}


// Press Enter to send
input.addEventListener("keydown", function(event) {

    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }

});