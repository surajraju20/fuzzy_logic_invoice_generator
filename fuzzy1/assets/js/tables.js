function addField(argument) {

    var i;
    for (i = 0; i < document.getElementById("copy").value; i++) {
        var myTable = document.getElementById("myTable");
        var currentIndex = myTable.rows.length-1;
        var currentRow = myTable.insertRow(-1);

        var dateBox = document.createElement("input");
        dateBox.setAttribute("name", "date" + currentIndex);
        dateBox.setAttribute("id", "date" + currentIndex);
        dateBox.setAttribute("type", "date");
        console.log(currentIndex);
        var data = document.getElementById("date"+String(currentIndex-1)).value;
        var got_date = new Date(data)
        var followingDay = new Date(got_date.getTime() + 86400000);
        console.log(followingDay)
        dateBox.setAttribute("value", followingDay);

        var feesBox = document.createElement("input");
        feesBox.setAttribute("name", "fees" + currentIndex);
        feesBox.setAttribute("id", "fees" + currentIndex);
        var data = document.getElementById("fees"+String(currentIndex-1)).value;
        feesBox.setAttribute("value", data);

        var travelBox = document.createElement("input");
        travelBox.setAttribute("name", "travel" + currentIndex);
        travelBox.setAttribute("id", "travel" + currentIndex);
        var data = document.getElementById("travel"+String(currentIndex-1)).value;
        travelBox.setAttribute("value", data);

        var foodBox = document.createElement("input");
        foodBox.setAttribute("id", "food" + currentIndex);
        foodBox.setAttribute("name", "food" + currentIndex);
        var data = document.getElementById("food"+String(currentIndex-1)).value;
        foodBox.setAttribute("value", data);

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