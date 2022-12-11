$(document).ready(function () {
    $('#classes').DataTable({
        paging: false,
        searching: false,
        infoCallback: false,
    });
});

function showInactive(){
    document.getElementById('inactiveContainer').style.display = "block";
    document.getElementById('inactiveToggleButton').textContent = "Hide Inactive Classes";
    document.getElementById('inactiveToggleButton').setAttribute( "onClick", "hideInactive();" );
}

function hideInactive(){
    document.getElementById('inactiveContainer').style.display = "none";
    document.getElementById('inactiveToggleButton').textContent = "Show Inactive Classes";
    document.getElementById('inactiveToggleButton').setAttribute( "onClick", "showInactive();" );
}