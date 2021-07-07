const es = new EventSource('http://localhost:12344/listen');
const rows_per_page = 18
const listener = function (event) {
    const type = event.type;
    var txt = `<tr><td>${type}</td><td>${event.data || es.url}</td></tr>`;
    window.console.log(txt);
    $("#root.log").prepend(txt);

    tbl = document.getElementById("root")
    var rows = tbl.rows.length;
    console.log("Rows = ", rows);
    if (rows > rows_per_page) {
        tbl.deleteRow(rows - 1);
    }

    if (type === 'result') {
    es.close();
    }
};

es.addEventListener('open', listener);
es.addEventListener('message', listener);
es.addEventListener('error', listener);
