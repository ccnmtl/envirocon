function hideNewMaterials() {
  if($("new_materials_list").innerHTML.replace(/^\s+|\s+$/g,"") == "") {
    hideElement("new_materials_list");
    $("new_materials_inner").innerHTML = "You have no new materials for this activity.";
  }
}

addLoadEvent(hideNewMaterials);