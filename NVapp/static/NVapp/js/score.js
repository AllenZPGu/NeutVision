var scores = {};

function createBtns(options) {
	for (var section in options) {
		var overallDiv = document.createElement("div");
		overallDiv.className = "overall_div"
		document.getElementById("rightPanel").appendChild(overallDiv);

		var newHead = document.createElement("h4");
		newHead.innerHTML = options[section]["heading"];
		overallDiv.appendChild(newHead);

		var newBtnHolder = document.createElement("div");
		newBtnHolder.className = "btn-group btn-group-justified";
		newBtnHolder.setAttribute("role", "group");
		overallDiv.appendChild(newBtnHolder);

		newBtnHolder.id=section
		scores[section]=null;

		for (var indivBtn in options[section]["buttons"]) {
			var newBtnG = document.createElement("div");
			newBtnG.className = "btn-group";
			newBtnHolder.setAttribute("role", "group");
			newBtnHolder.appendChild(newBtnG);

			var newBtn = document.createElement("button");
			newBtn.id = "btn_"+section+"_";
			newBtn.className = "btn btn-default assess";
			newBtn.setAttribute("type", "button");
			newBtn.innerHTML = options[section]["buttons"][indivBtn];
			newBtn.id = "btn_"+section+"_"+newBtn.innerHTML;
			newBtnG.appendChild(newBtn);
			newBtn.addEventListener("click",onBtnClick());
		}

		var inputDiv = document.createElement("div");
		inputDiv.className = "input_div";
		overallDiv.appendChild(inputDiv);
		inputDiv.appendChild(document.createElement("br"));

		var extraInput = document.createElement("input");
		extraInput.className = "form-control";
		extraInput.id = "input_"+section;
		extraInput.setAttribute("type", "text");
		extraInput.setAttribute("placeholder", "Extra comments")
		inputDiv.appendChild(extraInput)
		
		inputDiv.style.display = "none";

		overallDiv.appendChild(document.createElement("br"));
	}
}

function onBtnClick() {
	btns = document.getElementsByClassName("btn btn-default assess");
	for(var i = 0; i < btns.length; i++ ) {
		btns[i].onclick = onBtnClick2(btns[i]);
	}
}

function onBtnClick2(btn) {
	return function() {

		var btnHolder = btn.parentElement.parentElement;
		for (var j = 0; j < btnHolder.children.length; j++) {
			btnHolder.children[j].children[0].className = "btn btn-default assess";
		}
		btn.className = "btn btn-success assess";
		scores[btnHolder.id]=btn.innerHTML;

		var overallDiv = btnHolder.parentElement;
		for (var j = 0; j < overallDiv.children.length; j++){
			if (overallDiv.children[j].className == "input_div") {
				if (btn.innerHTML == "Other") {
					overallDiv.children[j].style.display = 'block';
				} else {
					overallDiv.children[j].style.display = 'none';
				}
			}
		}
	}
}

function onSubmit(image) {
	var proceed = true;
	for (i in scores) {
		if (scores[i]==null){
			proceed=false;
		} else if (scores[i]=="Other"){
			var commentsInput = document.getElementById("input_"+i);
			if (commentsInput != null){
				scores[i]="Other: "+commentsInput.value;
			}
		}
	}

	if (proceed) {
		scores["AllOtherComments"] = document.getElementById("input_extraComments").value;
		scores["Image"] = image;

		var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
		function csrfSafeMethod(method) {
			// these HTTP methods do not require CSRF protection
			return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		}
		$.ajaxSetup({
			beforeSend: function(xhr, settings) {
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
			}
		});
		$.ajax({
			url : "ajax/submit_score/",
			type : "POST",
			data : scores,
			success : function(suc) {
				if (suc['success']) {
					location.reload();
					alert("Success. Click OK to proceed to the next cell.");
				}
				else {
					alert("Something failed!!!");
				}
			}
		})
	} else {
		alert("Make sure you've selected an entry for every row.");
	}
}