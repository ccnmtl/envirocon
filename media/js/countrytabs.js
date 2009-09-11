function showFiles() {
  setStyle("data_panel", {'display':'none'});
  setStyle("files_panel", {'display':'block'});
  removeElementClass("files-tab", "off");
  removeElementClass("data-tab", "on");
  addElementClass("files-tab", "on");
  addElementClass("data-tab", "off");
}

function showData() {
  setStyle("files_panel", {'display':'none'});
  setStyle("data_panel", {'display':'block'});
  removeElementClass("files-tab", "on");
  removeElementClass("data-tab", "off");
  addElementClass("data-tab", "on");
  addElementClass("files-tab", "off");
}

function initCountryTabs() {
  connect("data-tab", "onclick", showData);
  connect("files-tab", "onclick", showFiles);
}

addLoadEvent(initCountryTabs);