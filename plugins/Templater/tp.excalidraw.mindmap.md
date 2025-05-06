<%*
class OutlineNode {
  constructor(depth, text, parent = -1) {
    this.depth = depth;
    this.text = text;
    this.parent = parent;
    this.size = 0;
    this.children = [];
    this.objectId = null;
  }
}

class OutlineParser {
  constructor(editor) {
    this.editor = editor;
  }
  
  parse() {
    const lineCount = this.editor.lineCount();
    if (lineCount === 0) {
      return [];
    }
    const nodes = [];
    let parents = [0];
    let validLineIndex = 0;
    const rootTitle = window.app.workspace.activeLeaf?.view?.getDisplayText() || "Untitled";
    const rootNode = new OutlineNode(0, rootTitle, -1);
    nodes.push(rootNode);
    for (let i = 0; i < lineCount; i++) {
      const props = this.editor.getLine(i).match(/^(\t*)-\s+(.*)/);
      if (!props) {
        continue;
      }
      const depth = props[1].length + 1;
      const text = props[2];
      if (depth > parents.length) {
        parents.push(validLineIndex + 1);
      } else {
        parents[depth] = validLineIndex + 1;
      }
      const node = new OutlineNode(depth, text, parents[depth - 1]);
      nodes.push(node);
      nodes[node.parent].children.push(validLineIndex + 1);
      validLineIndex++;
    }
    return nodes;
  }
}

class MindmapBuilder {
  constructor(ea, nodes) {
    this.ea = ea;
    this.nodes = nodes;
    this.width = 300;
    this.height = 100;
    this.colorList = ['#e03131', '#1971c2', '#099268', '#e8590c', '#9c36b5', '#6741d9', '#0c8599'];
    this.offsets = [0];
    this.colorIndex = 0;
    this.wikiImageList = [];
    this.direction = null;
    this.arrowType = null;
    this.backgroundColor = null;
  }
  
  computeSize(index) {
    if (index >= this.nodes.length) {
      return 0;
    }
    const node = this.nodes[index];
    if (index + 1 >= this.nodes.length || this.nodes[index + 1].depth <= node.depth) {
      node.size = 1;
      return 1;
    }
    let size = 0;
    node.children.forEach(childIndex => {
      size += this.computeSize(childIndex);
    });
    node.size = size;
    return size;
  }
  
  getFontSize(depth) {
    switch(depth) {
      case 0: return 48;
      case 1: return 32;
      case 2: return 20;
      default: return 20;
    }
  }
  
  async buildMindmap(fileName, folderName) {
    const directionOptions = ["LR","RL","TD","BU"];
    this.direction = await tp.system.suggester(
      directionOptions,
      directionOptions,
      false,
      "Please choose a direction for the mind map (Left->Right = LR, Right->Left = RL, Top->Down = TD, Bottom->Up = BU)"
    );
    const arrowOptions = ["normal","elbow"];
    this.arrowType = await tp.system.suggester(
      arrowOptions,
      arrowOptions,
      false,
      "Please choose an arrow type (normal or elbow)"
    );
    this.ea.reset();
    await this.ea.create({
      filename: fileName,
      foldername: folderName,
      onNewPane: true
    });
    setTimeout(async () => {
      this.ea.setView('active');
      this.ea.tools.assignNestedProperty(window, "customData.Mindmap.treeElements", []);
      this.ea.style.roundness = {type: 3};
      this.ea.style.fillStyle = "solid";
      this.ea.style.roughness = 0;
      this.ea.style.fontFamily = 2;
      this.computeSize(0);
      let rootId = null;
      for (let i = 0; i < this.nodes.length; i++) {
        const node = this.nodes[i];
        // console.log(`depth: ${node.depth}  text: ${node.text}`)
        this.applyNodeColorStyle(node.depth);
        this.ea.style.fontSize = this.getFontSize(node.depth);
        const x = node.depth * this.width;
        const y = ((node.size / 2) + this.offsets[node.depth]) * this.height;
        const [objectId, allElements, parseResult] = await this.ea.tools.addElementsByString(node.text, x, y, {
          box: true,
          textAlign: "center",
          textVerticalAlign: "middle",
          boxStrokeColor: "black"
        });
        node.objectId = objectId;
        parseResult.forEach((r, idx) => {
          if (r.type === "wikiLink") {
            const image = this.ea.imagesDict[allElements[idx].fileId];
            if (image.hyperlink && !image.hyperlink.startsWith('[[')) {
              this.wikiImageList.push(allElements[idx].fileId);
            }
          }
        });
        if (node.depth === 0) {
          rootId = node.objectId;
        }
        const el = this.ea.getElement(node.objectId);
        if (!el) continue;
        el.customData = {
          mindmap: {
            status: "open",
            root: rootId,
            parent: (node.parent !== -1) ? this.nodes[node.parent].objectId : rootId,
            level: node.depth + 1
          }
        };
        if (node.depth === 0) {
          el.customData.mindmap.style = {
            direction: this.direction || "LR",
            arrowType: this.arrowType || "elbow"
          };
        }
        window.customData.Mindmap.treeElements.push(el, ...allElements);
        if ((node.depth + 1) > this.offsets.length) {
          this.offsets.push(this.offsets[node.depth]);
        } else {
          this.offsets[node.depth + 1] = this.offsets[node.depth];
        }
        this.offsets[node.depth] += node.size;
        if (node.parent !== -1) {
          const parentNode = this.nodes[node.parent];
          const arrowId = this.ea.connectObjects(parentNode.objectId, "right", node.objectId, "left", {startArrowHead: 'dot'});
          const arrowEl = this.ea.getElement(arrowId);
          window.customData.Mindmap.treeElements.push(arrowEl);
        }
      }
      const elementsDict = this.ea.elementsDict;
      const imagesDict = this.ea.imagesDict;
      await this.ea.tools.runScript('Mindmap format2');
      this.ea.elementsDict = elementsDict;
      this.ea.imagesDict = imagesDict;
      this.wikiImageList.forEach(id => {
        const image = this.ea.imagesDict[id];
        image.hyperlink = `[[${image.hyperlink}]]`;
      });
      this.ea.addElementsToView(false, false);
    }, 100);
  }
  
  applyNodeColorStyle(depth) {
    if (depth === 0) {
      this.ea.style.strokeColor = "black";
      this.ea.style.backgroundColor = "#343a40";
      return;
    } else if (depth === 1) {
      const color = this.colorList[this.colorIndex % this.colorList.length];
      this.colorIndex++;
      this.ea.style.strokeColor = "black";
      this.ea.style.backgroundColor = color;
      this.backgroundColor = color;
      return;
    } else {
      const cm = this.ea.getCM(this.backgroundColor);
      this.ea.style.backgroundColor = cm.lighterBy((depth - 1) * 20).stringHEX({alpha:false});
    }
  }
}

(async () => {
  const editor = this.app.workspace.activeLeaf?.view?.editor;
  if (!editor) {
    return;
  }
  const filePath = await tp.system.prompt("File path?", app.workspace.activeLeaf.view.file.path.substring(0, app.workspace.activeLeaf.view.file.path.lastIndexOf(".")) + '_mindmap');
  const lastIndex = filePath.lastIndexOf("/");
  const fileName = filePath.substring(lastIndex + 1);
  const folderName = filePath.substring(0, lastIndex) || tp.file.folder() || '/';
  const parser = new OutlineParser(editor);
  const nodes = parser.parse();
  if (nodes.length === 0) {
    console.log("No content to build a mind map.");
    return;
  }
  const ea = window.ExcalidrawAutomate;
  const builder = new MindmapBuilder(ea, nodes);
  console.log(`fileName: ${fileName}, folderName: ${folderName}`);
  await builder.buildMindmap(fileName, folderName);
})();
%>