function addField(argument) {
    var myTable = document.getElementById("myTable");
    var currentIndex = myTable.rows.length;
    var currentRow = myTable.insertRow(-1);

    var dateBox = document.createElement("input");
    dateBox.setAttribute("name", "date" + currentIndex);
    dateBox.setAttribute("type", "date");

    var feesBox = document.createElement("input");
    feesBox.setAttribute("name", "fees" + currentIndex);

    var travelBox = document.createElement("input");
    travelBox.setAttribute("name", "travel" + currentIndex);

    var foodBox = document.createElement("input");
    foodBox.setAttribute("name", "food" + currentIndex);


    var i;
    for (i = 0; i < document.getElementById("copy").value; i++) {

        var addRowBox = document.createElement("input");
        addRowBox.setAttribute("type", "button");
        addRowBox.setAttribute("value", "Add another line");
        addRowBox.setAttribute("onclick", "addField();");
        addRowBox.setAttribute("class", "button");

        var currentCell = currentRow.insertCell(-1);
        currentCell.appendChild(dateBox);


        currentCell = currentRow.insertCell(-1);
        currentCell.appendChild(feesBox);

        currentCell = currentRow.insertCell(-1);
        currentCell.appendChild(travelBox);

        currentCell = currentRow.insertCell(-1);
        currentCell.appendChild(foodBox);

        currentCell = currentRow.insertCell(-1);
        currentCell.appendChild(addRowBox);


        document.createElement("br");
    }

}