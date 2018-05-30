function createTable(history) {
	var overallTable = document.createElement("table");
	overallTable.className = "table table-striped";
	document.getElementById("mainTableDiv").appendChild(overallTable);

	var newTHead = document.createElement("thead");
	overallTable.appendChild(newTHead);
}

function resortRows(history, sortBy) {
	console.log("Sad");
}