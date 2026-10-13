function search() {
    // 1. Récupération de la valeur de recherche et normalisation en minuscules
    var input = document.getElementById("recherche");
    if (!input) return; // Sécurité si le champ n'existe pas
    
    var filter = input.value.toLowerCase();

    // 2. Ciblage des div de classe "lastItem" au lieu des "li"
    // On utilise querySelectorAll pour sélectionner toutes les div avec cette classe
    var items = document.querySelectorAll(".lastItem");

    // 3. Boucle sur chaque élément trouvé
    items.forEach(function(item) {
        // On récupère le texte visible à l'intérieur de la div (nom de la playlist)
        // textContent récupère tout le texte, peu importe la balise (p, a, etc.)
        var textContent = item.textContent || item.innerText;
        
        // On compare le texte de l'élément avec la recherche
        if (textContent.toLowerCase().indexOf(filter) > -1) {
            // Si ça correspond, on affiche l'élément.
            // On remet un style vide ou 'block' pour laisser le CSS Grid (dans .lastItems) gérer l'affichage.
            item.style.display = ""; 
        } else {
            // Sinon, on cache l'élément
            item.style.display = "none";
        }
    });
}