function search(){

    //On crée une fonction qui va cacher notre ligne et qui prend un élément du document en paramètre (ici une li)
    function toggleDisplay(elmt){
        //Si l'élément n'est pas caché...
        if (elmt.style.display != "none"){
            //...On le cache
            elmt.style.display = "none";
        }
    }

    //On crée une fonction qui va montrer notre ligne et qui prend un élément du document en paramètre (ici une li)
    function inlineBlock(elmt){
        //Si l'élément n'est pas montré...
        if (elmt.style.display != "inline-block"){
            //...On le montre
            elmt.style.display = "inline-block";
        }
    }

    //On crée la variable de la boucle while et on la set à 0
    var i = 0;

    //On met la valeur du champs recherche dans la variable txt
    var txt = document.getElementById("recherche").value;

    //On met la valeur de txt dans txtFormat pour la mettre en minuscule
    var txtFormat = txt.toLowerCase();

    //On met la liste de tous les li dans la variable ul
    var ul = document.getElementById("listeGroupe");

    //On met chaque li dans une variable li
    var li = ul.getElementsByTagName("li");

    //Tant que la valeur de i est inférieur ou égale à la valeur maximale de la liste...
    while (i <= li.length){
        //On compare l'ID de la ligne numéro i avec la variable txt et on met le résultat dans la variable res
        var res = new RegExp(txtFormat.replace(/\s+/g, '|'), 'i').test(li[i].id);

        //Si la valeur de res est -1 (ce qui veut dire que txt n'est pas trouvé dans l'ID de la ligne en cours)...
        if (!res){
            //...On appelle notre fonction pour cacher la ligne
            toggleDisplay(li[i]);
            //On incrémente la valeur i de 1
            i++;
            //Sinon (txt a été trouvé dans l'ID)
        } else {
            //On appelle notre fonction pour montrer la ligne
            inlineBlock(li[i]);
            //On incrémente la valeur i de 1
            i++;
        }
    }
}

// Fonction d'ajout de formulaire ajoutant des morceaux à un albums
function addRow(event) {
    event.preventDefault(); // Prevent form submission

    var totalFormId = document.getElementById('id_track_set-TOTAL_FORMS'); // Management form
    var currentFormCount = parseInt(totalFormId.value); // Current number of forms
    var nbRow = parseInt(document.getElementById("nbRow").value); // Number of rows to add
    var submitButton = document.getElementById("submit-button"); // Submit button
    var formContainer = document.querySelector(".formTrack"); // Parent container

    var emptyForm = document.querySelector(".formTrackRow"); // Select the first existing form row
    if (!emptyForm) {
        console.error("No form row found!");
        return;
    }

    var regex = new RegExp('__prefix__', 'g'); // Regex for form prefix replacement

    for (var i = 0; i < nbRow; i++) {
        var clone = emptyForm.cloneNode(true); // Clone the form row
        var newFormIndex = currentFormCount + i; // Get new form index

        // Update IDs and names inside the cloned form
        clone.innerHTML = clone.innerHTML.replace(regex, newFormIndex);
        clone.setAttribute("id", `form-${newFormIndex}`);
        clone.classList.add("track-row"); // Add class for styling

        // Create delete button
        var btn = document.createElement("button");
        btn.innerHTML = "-";
        btn.setAttribute("class", "delete-row btn-delete");
        btn.setAttribute("type", "button");
        btn.setAttribute("onclick", `deleteRow('form-${newFormIndex}')`); // Pass correct ID

        clone.appendChild(btn); // Add delete button to form
        submitButton.before(clone); // Insert before submit button
    }

    // Update TOTAL_FORMS count
    totalFormId.value = currentFormCount + nbRow;
}

function deleteRow(formId){
    console.log(formId);
    var totalFormId = document.getElementById('id_track_set-TOTAL_FORMS');
    var f = document.getElementById(formId);
    f.remove();
    totalFormId.value -= 1;
}

function displayChart(){

    var chartList = document.getElementsByClassName("chart");// On récupère tous les graphs de la page dans chartList
    var selectedChart = document.getElementById("albumChartSelector").value;// On Récupère le nom du graph souhaités via la valeur du selecteur
    var familySelector = document.getElementById("familySelector");// On récupère la div qui contient le sélecteur de famille
    var i = 0;// On initialise l'incérmenteur de la boucle

    while (i < chartList.length) {// Tant que l'incrémenteur est inférieur au nombre de graphs
        id = chartList[i].id;// On récupère l'id du graph numéro i

        if (id == selectedChart) {// Si le id du graph en cours correspond à la valeur du selecteur
            chartList[i].style.display = "block";// On l'affiche

            if (id == "albumByGenre") { // Si le sélecteur est albumByGenre
                familySelector.style.display = "block"// Alors on affiche le sélecteur de famille
            } else {// Sinon
                familySelector.style.display = "none"// On le cache
            }

        } else {// Sinon
            chartList[i].style.display = "none"; //On le cache
        }

        i++;// On incrémente notre incrémenteur de 1
    }
}

function sortTable(n) {
  var rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  var table1 = document.getElementById("tableContainerDetails");
  var table2 = document.getElementById("displayFilterDetails");
  var table;

  if ( table1 === null) {
    table = table2;
  } else {
    table = table1;
  }
  console.log(table)
  switching = true;
  // Set the sorting direction to ascending:
  dir = "asc";
  /* Make a loop that will continue until
  no switching has been done: */
  while (switching) {
    // Start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /* Loop through all table rows (except the
    first, which contains table headers): */
    for (i = 1; i < (rows.length - 1); i++) {
      // Start by saying there should be no switching:
      shouldSwitch = false;
      /* Get the two elements you want to compare,
      one from current row and one from the next: */
      x = rows[i].getElementsByTagName("TD")[n].textContent;
      y = rows[i + 1].getElementsByTagName("TD")[n].textContent;
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == "asc") {
        if (x.toLowerCase() > y.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x.toLowerCase() < y.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /* If a switch has been marked, make the switch
      and mark that a switch has been done: */
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      // Each time a switch is done, increase this count by 1:
      switchcount ++;
    } else {
      /* If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again. */
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}