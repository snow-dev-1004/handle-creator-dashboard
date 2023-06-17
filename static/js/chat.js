let lastUpdatedTime = Date.now(),
  loading = false;

$(document).ready(function () {
  const chatScrollTop = () => {
    $(".msger-chat")[0].scrollTop = 10000000000;
  };

  const sendMessage = () => {
    let text = $(".msger-input")[0].innerHTML;
    $(".msger-input")[0].innerHTML = "";
    loading = true;
    $(".msger-send-loader").toggleClass("d-none");
    $(".msger-send-btn").toggleClass("d-none");

    let csrfToken = $("[name='csrfmiddlewaretoken']").val();
    text = text.replaceAll("<br>", "\n");
    let data = new FormData();
    data.append("message", text);
    data.append("csrfmiddlewaretoken", csrfToken);
    let ownerMessageTemplate = `
			<div class="msg right-msg">
				<div
					class="msg-img"
					style="
						background-image: url(https://image.flaticon.com/icons/svg/327/327779.svg);
					"
				></div>
				<div class="msg-bubble">
					<div class="msg-info">
						<div class="msg-info-name">${userFirstName}</div>
						<div class="msg-info-time">Just now</div>
					</div>
					<div class="msg-text">
						${text}
					</div>
				</div>
			</div>`;
    $(".msger-chat").append(ownerMessageTemplate);
    chatScrollTop();

    axios
      .post("/chat/", data)
      .then((res) => {
        loading = false;

        let botMessageTemplate = `
					<div class="msg left-msg">
						<div
							class="msg-img"
							style="
								background-image: url(https://image.flaticon.com/icons/svg/327/327779.svg);
							"
						></div>
						<div class="msg-bubble">
							<div class="msg-info">
								<div class="msg-info-name">Handle bot</div>
								<div class="msg-info-time">Just now</div>
							</div>
							<div class="msg-text">
								${res.data.data}
							</div>
						</div>
					</div>`;
        $(".msger-chat").append(botMessageTemplate);
        chatScrollTop();
        $(".msger-send-loader").toggleClass("d-none");
        $(".msger-send-btn").toggleClass("d-none");
      })
      .catch((errors) => {});
  };

  chatScrollTop();
  $(".msger-send-btn").click(function () {
    sendMessage();
  });
	$(document).on('keydown', (e) => {
		if (e.ctrlKey && e.keyCode == 13) {
			if ($('.msger-input').is(':focus')) {
				sendMessage();
			}			
		}
	})
});
