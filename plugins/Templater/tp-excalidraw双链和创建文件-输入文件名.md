<%*
const ea = ExcalidrawAutomate;
function getDrawingFilename(settings, fileName) {
    return (
        fileName +
        (settings.compatibilityMode
        ? ".excalidraw"
        : settings.useExcalidrawExtension
        ? ".excalidraw.md"
        : ".md")
    );
}

const filePath = await tp.system.prompt("File path?", app.workspace.activeLeaf.view.file.path.substring(0, app.workspace.activeLeaf.view.file.path.lastIndexOf(".")));
const lastIndex = filePath.lastIndexOf("/")
const fileName = filePath.substring(lastIndex + 1)
const folderName = fileName.substring(0, lastIndex) || tp.file.folder() || '/'
const path = await ea.plugin.createAndOpenDrawing(getDrawingFilename(ea.plugin.settings, fileName), "new-pane", folderName);
// const path = await ea.create({filename: fileName,foldername:tp.file.folder() || '/', onNewPane: true, templatePath: ea.plugin.settings.templateFilePath});
%>
# Title

<%*
return `[[${path}]]`
%>

Hello