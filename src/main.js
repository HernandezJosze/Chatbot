document.addEventListener('DOMContentLoaded', () => {
  const user = "Usuario"
  const chat_msgs = document.getElementById("chat-messages");
  const input_msgs = document.getElementById("message-input");

  function AppendToChat(sender, msg) {
    if(input_msgs.value === "") {
      return;
    }

    let new_input_msg = document.createElement("div");
    new_input_msg.textContent = sender + ": " + msg.value;
    chat_msgs.appendChild(new_input_msg);
    input_msgs.value = "";
    chat_msgs.scrollTop = chat_msgs.scrollHeight;
  };

  const enter_btn = document.getElementById("send-button");
  enter_btn.onclick = () => {
    AppendToChat(user, input_msgs);
  }

  input_msgs.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
      enter_btn.click();
    }
  });
});