function createTable(columns, history, imgPath) {
	var overallTable = document.createElement("table");
	overallTable.className = "table table-bordered table-striped";
	document.getElementById("mainTableDiv").appendChild(overallTable);

	var newTHead = document.createElement("thead");
	overallTable.appendChild(newTHead);
	overallTable.id = "overallTable";
	var newTRow = document.createElement("tr");
	newTHead.appendChild(newTRow);

	// var newTH = document.createElement("th");
	// newTH.setAttribute("scope","col");
	// newTH.innerHTML = "#";
	// newTRow.appendChild(newTH);

	for (var i=0; i<columns.length; i++) {
		var newTH = document.createElement("th");
		newTH.setAttribute("scope","col");
		newTH.innerHTML = columns[i];
		newTRow.appendChild(newTH);
	}

	newTBody = document.createElement("tbody");
	newTBody.id = "mainTBody";
	overallTable.appendChild(newTBody);

	reSortRows(columns, history, imgPath, "Date");

}

function reSortRows(columns, history, imgPath, sortBy) {

	for (var i=0; i<history.length; i++) {
		var newTR = document.createElement("tr");
		document.getElementById("mainTBody").appendChild(newTR);
		// newRowTH = document.createElement("th")
		// newRowTH.setAttribute("scope","row");
		// newTR.appendChild(newRowTH)

		for (var j=0; j<columns.length; j++) {
			var newTD = document.createElement("td");

			if (columns[j]=="Image") {
				neutName = document.createElement("a");
				neutName.setAttribute("href", "#");
				// neutName.setAttribute("rel", "popover");
				// neutName.setAttribute("title", "Popover Header");
				// neutName.setAttribute("data-img", imgPath+history[i][columns[j]]);
				neutName.innerHTML = history[i][columns[j]];
				newTD.appendChild(neutName);
			} else {
				newTD.innerHTML=history[i][columns[j]];
			}

			newTR.appendChild(newTD);
		}
	}
}

// $('a[rel=popover]').popover({
// 	html: true,
// 	trigger: 'click',
// 	placement: 'bottom',
// 	content: function(){return '<img src="{% static \''+$(this).data('img') + '\' %}">';}
// });