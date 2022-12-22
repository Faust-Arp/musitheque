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
        var res = li[i].id.indexOf(txtFormat);

        //Si la valeur de res est -1 (ce qui veut dire que txt n'est pas trouvé dans l'ID de la ligne en cours)...
        if (res == -1){
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
function addRow(){

    var emptyForm = document.querySelector('#empty-form');// Initialisation de la variable initiale avec le formulaire de base
    var i = 1;// Initialisation de la variable de la boucle avec pour valeur 1
    var nbRow = document.getElementById("nbRow").value;// Initialisation de la variable contenant la valeur du widget nombre de ligne
    var totalFormId = document.getElementById('id_track_set-TOTAL_FORMS');// Initialisation de la variable contenant le formulaire
    var currentFormCount = parseInt(totalFormId.value);// Initialisation du nombre de formulaire en cours sur la page
    var submitButton = document.getElementById("submit-button");// Initialisation du bouton de validation du formulaire pour pouvoir mettre les clones avant lui
    var regex = new RegExp('__prefix__', 'g')// Initialisation de la regular expression à changer dans le HTML des clones


    while (i <= nbRow){// Tant que i est inférieur ou égal à la variable du nombre de ligne

      var clone = emptyForm.cloneNode(true); // On crée un clone du formulaire de base

      var btn = document.createElement("button");// On crée un bouton qui servira à supprimer la ligne
      btn.innerHTML = '-';// On lui ajoute du texte
      btn.setAttribute('class', 'delete-row btn-delete');// On lui donne une class
      btn.setAttribute('type', 'button')// On lui donne le type button pour ne pas qu'il envoie le formulaire lors d'un clic
      btn.setAttribute('onclick', 'deleteRow()');// On lui ajoute le eventListener onclick qui appelle la fonction de suppression

      clone.setAttribute('class', 'track-row');// On change la classe du clone
      clone.setAttribute('id', `form-${currentFormCount}`);// On change l'ID du clone
      btn.setAttribute('onclick', 'deleteRow("'+clone.id+'")');// On ajoute le paramètre de la fonction avec le id du div qui contient la ligne
      clone.innerHTML = clone.innerHTML.replace(regex, currentFormCount)// On remplace la regular expression par le nombre de formulaire en cours
      clone.appendChild(btn);// On ajoute le bouton à la fin de la ligne

      submitButton.before(clone);// Et on l'ajoute avant le bouton submit

      i++;// On incérmente i de 1
      currentFormCount++;// On incérmente le nombre de formulaire en cours de 1
      totalFormId.setAttribute('value', currentFormCount)// On change la valeur de id_track_set-TOTAL_FORMS pour le nombre de formulaire
    }

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
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("displayDetails");
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
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      /* Check if the two rows should switch place,
      based on the direction, asc or desc: */
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
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