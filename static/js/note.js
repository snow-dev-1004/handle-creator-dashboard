let lastUpdatedTime = Date.now();

$(document).ready(function () {
  $("#note-content").dblclick(function () {
    let va = $("#note-content").attr("readOnly");
    if (va) {
      $("#note-content").attr("readOnly", false);
    } else {
      $("#note-content").attr("readOnly", true);
    }
  });

	$("#note-content").on('input', function (e) {
		lastUpdatedTime = Date.now();

		setTimeout(async () => {
			let deft = Date.now() - lastUpdatedTime;
			if (deft > 1000) {
				let data = new FormData();
				data.append('content', e.target.value);
				axios.post('/note', data, (res) => {
					console.log(res);
				})
			}
		}, 1000);
	})
});