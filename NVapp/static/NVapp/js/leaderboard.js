function createTable(columns, sortedList) {
	var overallTable = document.createElement("table");
	overallTable.className = "table table-bordered table-striped";
	document.getElementById("mainTableDiv").appendChild(overallTable);

	var newTHead = document.createElement("thead");
	overallTable.appendChild(newTHead);
	overallTable.id = "overallTable";
	var newTRow = document.createElement("tr");
	newTHead.appendChild(newTRow);

	for (var i=0; i<columns.length; i++) {
		var newTH = document.createElement("th");
		newTH.setAttribute("scope","col");
		newTH.innerHTML = columns[i];
		newTRow.appendChild(newTH);
	}

	newTBody = document.createElement("tbody");
	newTBody.id = "mainTBody";
	overallTable.appendChild(newTBody);

	reSortRows(columns, sortedList);

}

function reSortRows(columns, sortedList) {
	for (var i=0; i<sortedList.length; i++) {
		var newTR = document.createElement("tr");
		document.getElementById("mainTBody").appendChild(newTR);

		for (var j=0; j<columns.length; j++) {
			var newTD = document.createElement("td");
			newTD.innerHTML=sortedList[i][columns[j]];
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