<%*
const ea = ExcalidrawAutomate;
function getDrawingFilename(settings, fileName) {
    return (fileName +(settings.compatibilityMode? ".excalidraw": settings.useExcalidrawExtension? ".excalidraw.md": ".md"));
}
const currentFilePath = app.workspace.activeLeaf.view.file.path.substring(0, app.workspace.activeLeaf.view.file.path.lastIndexOf("."))
const lastIndex = currentFilePath.lastIndexOf("/")
const fileName = getDrawingFilename(ea.plugin.settings, currentFilePath.substring(lastIndex + 1))
const path = await ea.plugin.createAndOpenDrawing(fileName, "new-pane", 'example');
%>
<%`[[${path}|${fileName.slice(0, -3)}]]`%>
