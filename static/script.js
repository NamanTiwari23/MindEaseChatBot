async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    if (!message) return;

    input.value = '';

    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += `<div class="user"><strong>You:</strong> ${message}</div>`;

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        // ✅ Use innerHTML to allow HTML formatting (e.g., <b>, <br>, bullet points)
        chatBox.innerHTML += `<div class="bot"><strong>Bot:</strong> ${data.response}</div>`;
    } catch (error) {
        console.error('Error:', error);
        chatBox.innerHTML += `<div class="bot"><strong>Bot:</strong> Sorry, something went wrong.</div>`;
    }

    chatBox.scrollTop = chatBox.scrollHeight;
}
