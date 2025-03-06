document.addEventListener('DOMContentLoaded', () => {
  const user = "Usuario"
  const chatbot = "Chatbot"
  const chat_msgs = document.getElementById("chat-messages");
  const input_msgs = document.getElementById("message-input");
  const conversation_id = document.getElementById("conversation_id_input");
  //const apiURL = 'http://0.0.0.0:8000/chatbot'
  const apiUrl = 'https://relevant-powerful-stork.ngrok-free.app/chatbot'

  function AppendToChat(sender, msg) {
    if(msg === "") {
      return;
    }

    let new_input_msg = document.createElement("div");
    new_input_msg.textContent = sender + ": " + msg;
    chat_msgs.appendChild(new_input_msg);
    chat_msgs.appendChild(document.createElement("br"));
    chat_msgs.scrollTop = chat_msgs.scrollHeight;
  }

  const enter_btn = document.getElementById("send-button");
  enter_btn.onclick = async () => {
    const input = input_msgs.value;
    input_msgs.value = "";
    AppendToChat(user, input);

    await fetch(apiUrl + '?id=' + conversation_id.value + '&message=' + input,
        {method: "POST",
             mode: "no-cors"})
        .then(response => {
          if (!response.ok) {
            console.log(response);
            throw new Error('Network response was not ok');
          }
          return response.json();
        })
        .then(chatbot_res => {
          AppendToChat(chatbot, chatbot_res["message"].at(-1)["message"]);
          conversation_id.value = chatbot_res["conversation_id"];
          console.log(chatbot_res);
        })
        .catch(error => {
          console.error('Got an error:', error);
        });
  }

  input_msgs.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      enter_btn.click();
    }
  });
});